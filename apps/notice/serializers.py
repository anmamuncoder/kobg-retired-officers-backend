# apps/notice/serializers.py
from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "message",
            "is_featured",
            "is_active",
            "is_pinned",
            "expires_at",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        # auto set admin user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)