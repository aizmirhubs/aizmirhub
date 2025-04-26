from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Ekstra alanlar
    phone = models.CharField(max_length=15, blank=True, verbose_name="Telefon Numarası")
    
    # Meta bilgileri
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
    
    def get_full_name(self):
        """Tam adı döndürür"""
        return f"{self.first_name} {self.last_name}".strip()

# User referansı (opsiyonel)
User = CustomUser

# models.py
from django.db import models

class AIModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='models/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name