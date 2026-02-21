from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.base.models import BaseModel
from .constants import RANKS


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    # PERSONAL INFORMATION
    number_type = models.CharField(max_length=50, default='Service Number BA/BSS', blank=True, null=True)
    number = models.CharField(max_length=50, unique=True , blank=True, null=True)
    rank = models.CharField(max_length=50, choices=RANKS, blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    full_name = models.CharField(max_length=150, blank=True, null=True)
    decoration = models.CharField(max_length=100, blank=True, null=True)

    course_type = models.CharField(max_length=50, blank=True, null=True)
    course_number = models.CharField(max_length=50, blank=True, null=True)

    retirement_date = models.DateField(blank=True, null=True)
    ts_number = models.CharField(max_length=50, blank=True, null=True)

    # ADDRESS
    address_type = models.CharField(max_length=50, blank=True, null=True)
 
    present_address = models.JSONField(blank=True, null=True, default=dict, help_text="Store present address as JSON with keys: country, division, district, upazila_thana, street_address" )
    permanent_address = models.JSONField(blank=True, null=True,default=dict, help_text="Store permanent address as JSON with keys: country, division, district, upazila_thana, street_address" )

    # CONTACT
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    # NEXT OF KIN
    nok_name = models.CharField(max_length=150, blank=True, null=True)
    nok_phone = models.CharField(max_length=20, blank=True, null=True)
    nok_relation = models.CharField(max_length=50, blank=True, null=True)

    # AUTH FLAGS
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
