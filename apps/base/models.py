from django.db import models
import uuid

# Create your models here.

class BaseModel(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4,max_length=36,editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,null=True)
    updated_at = models.DateTimeField(auto_now=True,editable=False,null=True)

    class Meta:
        abstract = True
