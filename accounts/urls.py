from django.urls import path
from .views import (
    home,
    register,
    ShowroomView,  # showroom_view yerine bu!
    CustomLoginView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    welcome_view
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # Ana Sayfa
    path('', home, name='home'),

    # Kullanıcı İşlemleri
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Şifre Sıfırlama Akışı
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Diğer Sayfalar
    path('welcome/', welcome_view, name='welcome'),
    path('showroom/', ShowroomView.as_view(), name='showroom'),  # bu şekilde kullanmalısın
]
