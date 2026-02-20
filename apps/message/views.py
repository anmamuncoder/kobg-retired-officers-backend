from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from apps.base.permissions import MessagePermission 
from rest_framework.decorators import action

class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission]
    http_method_names = ["get", "post", "patch"]  # block PUT/DELETE

    def get_queryset(self):
        user = self.request.user

        # Admin sees all
        if user.is_staff or user.is_superuser:
            return Message.objects.all()

        # Officer never GETs, but safe fallback
        return Message.objects.filter(sender=user)

    @action(detail=True, methods=["patch"], url_path="mark-read")
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save(update_fields=["is_read"])

        return Response({"message": "Message marked as read"}, status=status.HTTP_200_OK )