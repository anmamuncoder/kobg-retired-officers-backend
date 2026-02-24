
from django.contrib import admin
from .models import Memory, MemoryPhoto

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "uploader", "created_at")
	search_fields = ("title", "uploader__full_name")
	list_filter = ("created_at", "uploader")
	filter_horizontal = ("tagged_friends",)

@admin.register(MemoryPhoto)
class MemoryPhotoAdmin(admin.ModelAdmin):
	list_display = ("id", "memory", "captured_at")
	search_fields = ("memory__title",)
	list_filter = ("captured_at",)
