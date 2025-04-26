from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from .models import AIModel

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from accounts.services.reset_password_service import send_reset_email

UserModel = get_user_model()

print("Views yüklendi")  # test amaçlı

# Anasayfa
def home(request):
    return render(request, 'home.html')

@login_required
def welcome_view(request):
    return render(request, 'registration/welcome.html')


# Kayıt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Giriş
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        print("Giriş formu geçerli, kullanıcı giriş yapıyor...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Giriş formu geçersiz:", form.errors)
        return super().form_invalid(form)


# Şifre Sıfırla - Adım 1
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        request = self.request
        UserModel = get_user_model()

        try:
            user = UserModel.objects.filter(email=email).first()
            if user:
                result = send_reset_email(request=request, user=user)
                if not result.get("success"):
                    if result.get("reason") == "Too frequent":
                        messages.warning(request, "Bu e-posta adresine kısa süre önce zaten bir şifre sıfırlama bağlantısı gönderildi. Lütfen biraz bekleyin.", extra_tags='password_reset')
                        return redirect('password_reset')
        except UserModel.DoesNotExist:
            pass

        messages.success(request, "Eğer bu e-posta ile kayıtlı bir kullanıcı varsa, şifre sıfırlama bağlantısı gönderildi.", extra_tags='password_reset')
        return redirect(self.success_url)


# Şifre Sıfırla - Adım 2
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(FormView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            self.user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            self.user = None

        if self.user is not None and default_token_generator.check_token(self.user, token):
            return super().dispatch(request, uidb64=uidb64, token=token, *args, **kwargs)
        else:
            return self.token_expired_response()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Şifreniz başarıyla güncellendi. Giriş yapabilirsiniz.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Şifre güncelleme başarısız oldu. Lütfen kurallara dikkat edin.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def token_expired_response(self):
        return render(self.request, 'registration/password_reset_link_expired.html')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        return redirect('login')


# Showroom View
class ShowroomView(TemplateView):
    template_name = 'showroom.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range'] = range(8)
        return context


# Micro AI Ajan View
class MicroAIAjansView(TemplateView):
    template_name = 'microaiajans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Micro AI Ajan Sayfası"
        context['features'] = ["Özellik 1", "Özellik 2", "Özellik 3"]
        return context

def showroom(request):
    models = AIModel.objects.all()
    return render(request, 'showroom.html', {'models': models})