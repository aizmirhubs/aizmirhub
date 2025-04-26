from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.templatetags.static import static
from datetime import timedelta


sent_tokens_cache = {}  # 10 dakika önlemli gönderim

# ⚠️ Token süresi dakika cinsinden
TOKEN_VALIDITY_MINUTES = 10  # 1 saat

def send_reset_email(request, user):
    """
    Şifre sıfırlama e-postası gönderir.
    Aynı kullanıcıya 10 dakika içinde tekrar gönderilmez.
    """
    now = timezone.localtime()
    user_email = user.email.lower()

    # 1. Kısa süre içinde tekrar gönderimi engelle
    last_sent = sent_tokens_cache.get(user_email)
    if last_sent and now - last_sent < timedelta(minutes=10):
        print(f"⏳ {user_email} adresine çok yakın zamanda zaten mail gönderilmiş.")
        return {"success": False, "reason": "Too frequent"}

    # 2. Token & UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # 3. Reset bağlantısı
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    reset_link = f"{protocol}://{domain}{reset_path}"

 

    # 4. Logo URL'si (statik klasörden mutlak URL olarak)
    logo_url = request.build_absolute_uri(static("images/LogoBeyaz.png"))

    # 5. Mail context
    context = {
        'user': user,
        'uid': uid,
        'token': token,
        'reset_link': reset_link,
        'domain': domain,
        'protocol': protocol,
        'site_name': current_site.name or "AIzmir Hub",
        'form_id': 'password-reset-form',
        'logo_url': logo_url,
        'token_validity_minutes': TOKEN_VALIDITY_MINUTES,
        'expires_at': (now + timedelta(minutes=TOKEN_VALIDITY_MINUTES)).strftime("%H:%M")


        

    }

    # 6. Mail içeriği
    subject = f"{context['site_name']} - Şifre Sıfırlama Talebi"
    html_content = render_to_string('registration/password_reset_email.html', context)
    text_content = f"""Merhaba {user.get_full_name() or user.username},

Şifre sıfırlama isteğinde bulundunuz.

Eğer bu isteği siz yaptıysanız aşağıdaki bağlantıya tıklayarak yeni bir şifre oluşturabilirsiniz:

{reset_link}

Eğer bu isteği siz yapmadıysanız, bu e-postayı dikkate almayınız.

Teşekkürler,
{context['site_name']} Ekibi
"""

    # 7. Gönderim (try/except ile hata kontrolü)
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # 8. Cache'e kaydet
        sent_tokens_cache[user_email] = now
        print(f"✅ {user_email} adresine şifre sıfırlama maili GÖNDERİLDİ.")
        return {"success": True}

    except Exception as e:
        print(f"❌ {user_email} adresine mail gönderilemedi. Hata: {str(e)}")
        return {"success": False, "reason": str(e)}
