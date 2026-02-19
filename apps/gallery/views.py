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
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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


class MemoryPhotoUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, memory_id):
        memory = get_object_or_404(Memory, id=memory_id)

        # Permission check
        if not request.user.is_staff and memory.uploader != request.user:
            return Response(
                {"detail": "You cannot upload photos to this memory."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MemoryPhotoSerializer(
            data=request.data,
            context={
                "request": request,
                "memory": memory
            }
        )
        serializer.is_valid(raise_exception=True)
        photo = serializer.save()

        return Response(
            {
                "message": "Photo uploaded successfully",
                "photo_id": photo.id
            },
            status=status.HTTP_201_CREATED
        )