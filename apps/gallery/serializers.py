from rest_framework.serializers import ModelSerializer

from rest_framework import serializers
from .models import Memory, MemoryPhoto

from apps.user.models import User

class MemoryPhotoSerializer(ModelSerializer):
    class Meta:
        model = MemoryPhoto
        fields = ["id", "image", "captured_at"]
        read_only_fields = ("id",)


class MemorySerializer(ModelSerializer):
    photos = MemoryPhotoSerializer(many=True, read_only=True)
    tagged_friends = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all(),required=False)

    class Meta:
        model = Memory
        fields = [
            "id",
            "title",
            "description",
            "tagged_friends",
            "created_at",
            "photos"
        ]
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        tagged_friends = validated_data.pop("tagged_friends", [])
        memory = Memory.objects.create(
            uploader=self.context["request"].user,
            **validated_data
        )
        memory.tagged_friends.set(tagged_friends)
        return memory
    
