from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import AIModel

admin.site.register(CustomUser, UserAdmin)

admin.site.register(AIModel)
