from rest_framework.serializers import ModelSerializer

from rest_framework import serializers
from .models import Memory, MemoryPhoto

from apps.user.models import User


class TaggedFriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "number",
            "number_type",
            "rank",
        ]

class MemoryPhotoSerializer(ModelSerializer):
    class Meta:
        model = MemoryPhoto
        fields = ["id", "image", "captured_at"]
        read_only_fields = ("id",) 

    def create(self, validated_data):
        memory = self.context["memory"]
        return MemoryPhoto.objects.create(memory=memory, **validated_data)
    

class MemorySerializer(ModelSerializer):
    photos = MemoryPhotoSerializer(many=True, read_only=True)
    tagged_friends = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all(),required=False)

    tagged_friends_details = TaggedFriendSerializer(source="tagged_friends",many=True,read_only=True)
 
    class Meta:
        model = Memory
        fields = [
            "id",
            "title",
            "description",
            "tagged_friends",  # write-only
            "tagged_friends_details", # read-only
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
    
