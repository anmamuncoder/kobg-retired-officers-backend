from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import index
urlpatterns_apps = [
    path('users/', include('apps.user.urls')),
    path('officer/', include('apps.officer.urls')),
    path('notice/', include('apps.notice.urls')),
    path('memory/', include('apps.gallery.urls')),
    path('message/', include('apps.message.urls')),
    path('course/', include('apps.course.urls')),
]

app_name = 'core'
urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('', index, name='index'),
    ]
    + urlpatterns_apps
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)