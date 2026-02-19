from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField
from rest_framework.exceptions import ValidationError
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','number_type', 'number', 'rank', 'full_name', 'decoration', 'course_type', 'course_number', 'retirement_date', 'ts_number', 'address_type', 'phone', 'whatsapp_number',  'nok_name', 'nok_phone', 'nok_relation','is_staff','is_active']
        read_only_fields = ('id', 'created_at', 'updated_at','is_staff','is_active')


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'number_type', 'number', 'rank', 'full_name', 'decoration', 
                  'course_type', 'course_number', 'retirement_date', 'ts_number', 'address_type', 'phone', 
                  'whatsapp_number', 'nok_name', 'nok_phone', 'nok_relation']
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data
        )
        user.is_active = False  
        user.save()
        return user


class UserLoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid email or password")
        
        if not user.check_password(password):
            raise ValidationError("Invalid email or password")
        
        if not user.is_active:
            raise ValidationError("User account is not active")
        
        data['user'] = user
        return data

# ----------------------------------------
# Admin only
# ----------------------------------------

class AdminCreationSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'number_type', 'number', 'phone', 'whatsapp_number']
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        admin_user = User.objects.create_user(
            email=email,
            password=password,
            **validated_data
        )
        admin_user.is_active = True  # Admin users are active by default
        admin_user.is_staff = True
        admin_user.is_superuser = False  # Not superuser, just staff
        admin_user.save()
        return admin_user


