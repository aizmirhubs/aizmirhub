from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Uygulama URL’lerini dahil et
    path('', include('accounts.urls')),
    path('', include('django.contrib.auth.urls')),

    # Sabit sayfalar (template-based)
    path('consulting/', TemplateView.as_view(template_name='consulting.html'), name='consulting'),
    path('saas/', TemplateView.as_view(template_name='saas.html'), name='saas'),
    path('aizmirdream/', TemplateView.as_view(template_name='aizmirdream.html'), name='aizmirdream'),
    path('microaiajans/', TemplateView.as_view(template_name='microaiajans.html'), name='microaiajans'),
    path('otomasyon/', TemplateView.as_view(template_name='otomasyon.html'), name='otomasyon'),
]

# Geliştirme ortamı için medya dosyalarını servis et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
