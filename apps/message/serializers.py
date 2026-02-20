from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Message

class MessageSerializer(ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "subject",
            "body",
            "is_read",
            "sender",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)