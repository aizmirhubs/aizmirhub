"""
Django settings for aizmirhub project.
"""
from decouple import config #eklendi
from pathlib import Path
import os


# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-your-secret-key-here'  # Change for production!
DEBUG = True
ALLOWED_HOSTS =  ['13.60.93.222', 'aizmirhub.com', 'www.aizmirhub.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'widget_tweaks',
    
    
    # Local apps
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aizmirhub.urls'

 
TEMPLATES = [  
    {  
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  
        'DIRS': [  
            BASE_DIR / 'templates',  # Ana dizindeki templates klasörü  
            BASE_DIR / 'accounts' / 'templates',  # accounts uygulamasındaki templates klasörü  
        ],  
        'APP_DIRS': True,  
        'OPTIONS': {  
            'context_processors': [  
                'django.template.context_processors.debug',  
                'django.template.context_processors.request',  
                'django.contrib.auth.context_processors.auth',  
                'django.contrib.messages.context_processors.messages',  
            ],  
        },  
    },  
]  

WSGI_APPLICATION = 'aizmirhub.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/login/'  # veya senin login view’ının tam yolu
LOGIN_REDIRECT_URL = '/'  # girişten sonra yönlendirme
LOGOUT_REDIRECT_URL = '/login/'  # çıkıştan sonra yönlendirme

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings (development)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aizmirhub@gmail.com'  # kendi e-posta adresin
EMAIL_HOST_PASSWORD = 'pqad ppgk nvyq tnfz'     # Gmail'den alınan uygulama şifresi
DEFAULT_FROM_EMAIL = 'AIzmir Hub <aizmirhub@gmail.com>'
# settings.py
PASSWORD_RESET_TIMEOUT = 600  # saniye cinsinden (600 saniye = 10 dakika)





# Site framework
SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

