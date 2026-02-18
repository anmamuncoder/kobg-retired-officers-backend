from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserView, UserRegistrationView, UserLoginView, UserProfileView, UserApprovalView, AdminCreationView

router = DefaultRouter() 
router.register('profile',UserProfileView,basename='profile')

app_name = 'user'
urlpatterns = (
    [
        path('list/',UserView.as_view(),name='user-list'),
        
        path('register/', UserRegistrationView.as_view(), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        
        path('approve/', UserApprovalView.as_view(), name='approve'),
        path('create-admin/', AdminCreationView.as_view(), name='create-admin'),
    ] + router.urls
)

