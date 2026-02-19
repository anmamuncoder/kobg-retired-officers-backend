from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Memory, MemoryPhoto
from .serializers import (
    MemorySerializer,
    MemoryPhotoSerializer
)

class MemoryViewSet(viewsets.ModelViewSet):
    serializer_class = MemorySerializer
    queryset = Memory.objects.all()
    
    def get_queryset(self):
            user = self.request.user

            # Admin / Superuser can see all memories
            if user.is_staff or user.is_superuser:
                return self.queryset

            # Normal user sees only his own memories
            return self.queryset.filter(uploader=user)
    

    @action(detail=True, methods=["post"], url_path="photos")
    def upload_photos(self, request, pk=None):
        memory = self.get_object()
        serializer = MemoryPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data["images"]
        captured_at = serializer.validated_data.get("captured_at")

        photos = []
        for img in images:
            photo = MemoryPhoto.objects.create(memory=memory,image=img,captured_at=captured_at)
            photos.append(photo)

        return Response({"message": f"{len(photos)} photos uploaded"},status=status.HTTP_201_CREATED)
