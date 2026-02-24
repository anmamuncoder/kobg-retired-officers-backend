from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User
from apps.gallery.models import Memory, MemoryPhoto

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','email','number_type', 'number', 'rank', 'full_name', 'decoration','photo' ,'course_type', 'course_number', 'retirement_date', 'ts_number', 'address_type', 'present_address', 'permanent_address',
                  'phone', 'whatsapp_number',  'nok_name', 'nok_phone', 'nok_relation','is_staff','is_active', 'created_at', 'updated_at',]
        read_only_fields = ('id', 'created_at', 'updated_at','is_staff','is_active')


class UserRetrieveSerializer(ModelSerializer):
    tagged_memorys = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email','number_type', 'number', 'rank', 'full_name', 'decoration','photo' ,'course_type', 'course_number', 'retirement_date', 'ts_number', 'address_type', 'present_address', 'permanent_address',
                  'phone', 'whatsapp_number',  'nok_name', 'nok_phone', 'nok_relation','is_staff','is_active','created_at', 'updated_at', 'tagged_memorys']
        read_only_fields = ('id', 'created_at', 'updated_at','is_staff','is_active','tagged_memorys')

    def get_tagged_memorys(self, obj):
        tagged_memories = Memory.objects.filter(tagged_friends=obj)
        result = []
        for memory in tagged_memories:
            photos = MemoryPhoto.objects.filter(memory=memory)
            photo_list = [
                {
                    "id": photo.id,
                    "image": photo.image.url if photo.image else None,
                    "captured_at": photo.captured_at
                }
                for photo in photos
            ]
            result.append({
                "tag_by": {
                    "id": obj.id,
                    "name": obj.full_name,
                    "rank_type": obj.number_type,
                    "rank": obj.rank,
                    "decoration": obj.decoration,
                },
                "memory_id": memory.id,
                "photos": photo_list
            })
        return result



class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'number_type', 'number', 'rank', 'full_name', 'decoration', 'photo',
                  'course_type', 'course_number', 'retirement_date', 'ts_number', 'address_type', 'present_address', 'permanent_address',
                  'phone','whatsapp_number', 'nok_name', 'nok_phone', 'nok_relation']
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


