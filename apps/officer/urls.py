from django.urls import path

from apps.officer.views import ActiveAccessOfficerView

app_name = 'officer'
urlpatterns = [
    path('active-access/', ActiveAccessOfficerView.as_view(), name='active_access_officers'),
]

