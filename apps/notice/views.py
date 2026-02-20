from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Notice
from .serializers import NoticeSerializer
from apps.base.permissions import IsAdminOrReadOnly
from django.db.models import Q

class NoticeViewSet(ModelViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        now = timezone.now()

        # users see only active & not expired notices
        return (
            Notice.objects
            .filter(is_active=True)
            .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=now))
            .order_by("-is_pinned", "-is_featured", "-created_at")
        )