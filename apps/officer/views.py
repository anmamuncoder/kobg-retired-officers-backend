from django.shortcuts import render
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils import timezone

# Create your views here.
from apps.user.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token

class ActiveAccessOfficerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Blacklisted tokens
        blacklisted_tokens = BlacklistedToken.objects.select_related('token').all()
        blacklisted_user_ids = set(token.token.user_id for token in blacklisted_tokens)
        blacklisted_users = User.objects.filter(id__in=blacklisted_user_ids)
        count_blacklisted = blacklisted_users.count()

        # Active refresh tokens (not blacklisted, not expired)
        now = timezone.now()
        active_refresh_tokens = OutstandingToken.objects.filter(
            expires_at__gt=now
        ).exclude(
            id__in=BlacklistedToken.objects.values_list('token_id', flat=True)
        )
        active_refresh_user_ids = set(token.user_id for token in active_refresh_tokens)
        active_refresh_users = User.objects.filter(id__in=active_refresh_user_ids, is_active=True)
        count_active_refresh = active_refresh_users.count()

        data = {
            'blacklisted_access_officers': count_blacklisted,
            'blacklisted_user_ids': list(blacklisted_user_ids),
            'active_refresh_officers': count_active_refresh,
            'active_refresh_user_ids': list(active_refresh_user_ids),
        }
        return Response(data, status=status.HTTP_200_OK)