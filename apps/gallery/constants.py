import os
import uuid
from django.conf import settings
from django.utils.text import slugify


def memory_photo_upload_path(instance, filename):
    """
    media/memories/user_<id>/<memory-title>/<title>_<unique>.jpg
    """
    user_id = instance.memory.uploader.id
    title_slug = slugify(instance.memory.title)

    ext = filename.split('.')[-1]
    unique_name = uuid.uuid4().hex[:10]

    filename = f"{title_slug}_{unique_name}.{ext}"

    return os.path.join("memories",f"user_{user_id}",title_slug,filename)
