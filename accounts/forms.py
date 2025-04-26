from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

from .models import CustomUser
from accounts.services import reset_password_service
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-posta",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ornek@email.com'
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kullanıcı adınız'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Şifreniz'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Şifrenizi tekrar girin'
        })


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Kullanıcı adınız veya e-posta'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Şifreniz'
        })


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-posta",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kayıtlı e-posta adresiniz'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresine ait bir kullanıcı bulunamadı.")
        return email

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False,
             token_generator=None,
             from_email=None,
             request=None,
             html_email_template_name=None,
             extra_email_context=None):

        # Django’nun kendi reset işlemi
        super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context,
        )

        # Özel e-posta servisini çağır
        email = self.cleaned_data["email"]
        reset_password_service.send_reset_email(request, email)


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user

    new_password1 = forms.CharField(
        label="Yeni Şifre",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifreniz'
        })
    )
    new_password2 = forms.CharField(
        label="Yeni Şifre (Tekrar)",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifrenizi tekrar girin'
        })
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')

        # Şifre kuralları
        if len(password) < 8:
            raise ValidationError("Şifre en az 8 karakter olmalıdır.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Şifre en az bir büyük harf içermelidir.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Şifre en az bir küçük harf içermelidir.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Şifre en az bir rakam içermelidir.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Şifre en az bir özel karakter içermelidir.")

        return password

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user