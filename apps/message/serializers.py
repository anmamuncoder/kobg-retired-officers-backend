from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Message
from .models import MessageReply

class MessageReplySerializer(ModelSerializer):
    # keep sender/message as writable/read-only model relations internally,
    # but conditionally remove them from the serialized output for non-admin users
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    message = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MessageReply
        fields = [
            "id",
            "message",
            "body",
            "sender",
            "created_at",
        ]
        read_only_fields = ("id", "created_at", "message", "sender")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request") if hasattr(self, "context") else None
        user = getattr(request, "user", None) if request is not None else None

        # If the requester is not an admin, hide `message` and `sender` from output
        if not (user and (getattr(user, "is_staff", False) or getattr(user, "is_superuser", False))):
            self.fields.pop("message", None)
            self.fields.pop("sender", None)

    def create(self, validated_data):
        # Ensure sender is set from request user even when sender field is not present in input
        request = self.context.get("request") if hasattr(self, "context") else None
        if request and getattr(request, "user", None):
            validated_data["sender"] = request.user
        return super().create(validated_data)

class MessageSerializer(ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = MessageReplySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "subject",
            "body",
            "is_read",
            "sender",
            "created_at",
            "replies",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)


