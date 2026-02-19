from django.db import models

# Create your models here.
from apps.user.models import User
from django.db import models
from .constants import memory_photo_upload_path
from apps.base.models import BaseModel

class Memory(BaseModel):
    uploader = models.ForeignKey(User,on_delete=models.CASCADE,related_name="uploaded_memories")
    title = models.CharField(max_length=255)
    tagged_friends = models.ManyToManyField(User,blank=True,related_name="tagged_memories")
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.title

class MemoryPhoto(BaseModel):
    memory = models.ForeignKey(Memory,on_delete=models.CASCADE,related_name="photos")
    image = models.ImageField(upload_to=memory_photo_upload_path)
    captured_at = models.DateTimeField(null=True,blank=True,help_text="Date and time when the photo was captured")

    def __str__(self):
        return f"Photo - {self.memory.title}"
