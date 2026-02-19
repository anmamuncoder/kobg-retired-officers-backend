from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MemoryViewSet


router = DefaultRouter()
router.register("memories", MemoryViewSet, basename="memory")

app_name = 'gallery'
urlpatterns = [
    
] 
urlpatterns += router.urls


