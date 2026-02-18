from django.contrib import admin

# Register your models here.
from .models import User

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'number', 'rank', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'number']
    list_filter = ['rank', 'is_active', 'is_staff']
    ordering = ['email']