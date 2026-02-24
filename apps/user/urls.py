from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserView, UserRegistrationView, UserLoginView, UserProfileView, UserApprovalView, AdminCreationView, UserRejectView

router = DefaultRouter() 
router.register('profile',UserProfileView,basename='profile')
router.register('list',UserView,basename='user-list')

app_name = 'user'
urlpatterns = (
    [ 
        
        
        path('register/', UserRegistrationView.as_view(), name='register'),
        path('login/', UserLoginView.as_view(), name='login'),
        
        path('create-admin/', AdminCreationView.as_view(), name='create-admin'),

        path('approve/', UserApprovalView.as_view(), name='approve'),
        path('reject/', UserRejectView.as_view(), name='reject'),
        
    ] + router.urls
)

