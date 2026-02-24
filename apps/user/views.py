from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserRetrieveSerializer, UserSerializer, UserRetrieveSerializer, UserRegistrationSerializer, UserLoginSerializer, AdminCreationSerializer
# Create your views here.


class UserView(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserRetrieveSerializer
        return UserSerializer

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully. Please wait for admin approval.',
                'user': serializer.data
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email, 
                'access_key': access_token,
                'refresh_key': refresh_token,
                'is_staff': user.is_staff
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
 

class UserProfileView(ModelViewSet):
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch'] 

    def get_queryset(self): 
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer): 
        if self.request.user != serializer.instance:
            raise PermissionDenied("You can update only your own profile.")
        serializer.save()



# ----------------------------------------
# Admin only
# ----------------------------------------
from django.core.mail import send_mail
from django.conf import settings

class UserApprovalView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """
        Approve/Activate a user account. Only staff/admin users can use this endpoint.
        Request body should contain: {"user_id": "user_id_here"}
        """
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({
                'error': 'user_id is required'
            }, status=HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)
        
        if user.is_active:
            return Response({
                'message': 'User is already active',
                'user_id': user.id,
                'email': user.email, 
                'is_active': user.is_active
            }, status=HTTP_200_OK)
        
        # Activate the user
        user.is_active = True
        user.save()
        
        try: 
            send_mail(
                subject='Your Account Has Been Approved',
                message=(
                    f'Hello {user.number_type} {user.number} {user.full_name} {user.rank},\n\n'
                    'Your account has been approved by the admin.\n'
                    'You can now login to the system.\n\n'
                    'Thank you.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Email failed:", e)

        return Response({
            'message': 'User approved and activated successfully',
            'user_id': user.id,
            'email': user.email, 
            'is_active': user.is_active
        }, status=HTTP_200_OK)

# User rejection API
class UserRejectView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Reject/Deactivate a user account. Only staff/admin users can use this endpoint.
        Request body should contain: {"user_id": "user_id_here", "reason": "reason for rejection"}
        """
        user_id = request.data.get('user_id')
        reason = request.data.get('reason')

        if not user_id:
            return Response({
                'error': 'user_id is required'
            }, status=HTTP_400_BAD_REQUEST)
        if not reason:
            return Response({
                'error': 'reason is required'
            }, status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            user_email = user.email
            user_is_active = user.is_active

        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=HTTP_404_NOT_FOUND)

        # Deactivate the user
        user.is_active = False
        user.save(update_fields=['is_active'])

        if user and user_is_active:
            return Response({
                'message': 'Deactivated user successfully',
                'user_id': user_id,
                'email': user_email,
                'is_active': user_is_active
            }, status=HTTP_200_OK)
        
        # -------------------------------------------------------------
        # Send rejection email to the user with the reason for rejection
        # -------------------------------------------------------------

        try:
            send_mail(
                subject='Your Account Has Been Rejected',
                message=(
                    f'Hello {user.number_type} {user.number} {user.full_name} {user.rank},\n\n'
                    'Your account has been rejected by the admin.\n'
                    f'Reason: {reason}\n\n'
                    'If you have questions, please contact support.\n\n'
                    'Thank you.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Email failed:", e)

        user.delete()  # Permanently delete the user from the database
        return Response({
                'message': 'User rejected and deleted successfully',
                'user_id': user_id,
                'email': user_email,
                'is_active': user_is_active,
                'reason': reason
        }, status=HTTP_200_OK)


class AdminCreationView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """
        Create a new admin/staff user. Only existing admin users can create new admins. 
        """
        serializer = AdminCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Admin user created successfully',
                'admin': {
                    'id': serializer.data['id'],
                    'email': serializer.data['email'],
                    'number_type': serializer.data['number_type'],
                    'number': serializer.data['number'],
                    'phone': serializer.data['phone'],
                    'whatsapp_number': serializer.data['whatsapp_number'],
                    'is_active': True,
                    'is_staff': True
                }
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)