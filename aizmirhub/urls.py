from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HubEventView  # 🔥 ÖNEMLİ: Bu satırı ekleyin!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('django.contrib.auth.urls')),
    path('consulting/', TemplateView.as_view(template_name='consulting.html'), name='consulting'),
    path('saas/', TemplateView.as_view(template_name='saas.html'), name='saas'),
    path('aizmirdream/', TemplateView.as_view(template_name='aizmirdream.html'), name='aizmirdream'),
    path('hubevent/', HubEventView.as_view(), name='hubevent'),  
    path('otomasyon/', TemplateView.as_view(template_name='otomasyon.html'), name='otomasyon'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)