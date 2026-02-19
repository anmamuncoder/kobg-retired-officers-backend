from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MemoryPhotoUploadAPIView, MemoryViewSet


router = DefaultRouter()
router.register("memories", MemoryViewSet, basename="memory")

app_name = 'gallery'
urlpatterns = [
    path("memories/<uuid:memory_id>/photos/", MemoryPhotoUploadAPIView.as_view()),
 
] 
urlpatterns += router.urls


