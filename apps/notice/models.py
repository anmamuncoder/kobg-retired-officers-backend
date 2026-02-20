from django.db import models
 
from django.db import models
from apps.base.models import BaseModel
from apps.user.models import User


class Notice(BaseModel):

    title = models.CharField(max_length=255)
    message = models.TextField()

    # feature flag (important notice)
    is_featured = models.BooleanField(default=False)

    # active / inactive (soft hide)
    is_active = models.BooleanField(default=True)

    # pin to top
    is_pinned = models.BooleanField(default=False)

    # optional expiry
    expires_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_notices"
    )

    def __str__(self):
        return self.title