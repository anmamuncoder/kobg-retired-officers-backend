from django.db import models
from apps.base.models import BaseModel

# Create your models here.
class Course(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField() 
    order = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.name