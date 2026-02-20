from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MessageView

router = DefaultRouter()
router.register("messages", MessageView, basename="message")

 
app_name = 'message'
urlpatterns = [
    
]
urlpatterns = router.urls


