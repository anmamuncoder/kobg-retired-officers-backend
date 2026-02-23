from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from apps.base.permissions import IsAdminOrReadOnly

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('order')
    serializer_class = CourseSerializer 
    permission_classes = [IsAdminOrReadOnly]
    