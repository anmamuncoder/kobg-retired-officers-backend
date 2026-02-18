from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns_apps = [
    path('users/', include('apps.user.urls')),
    path('officer/', include('apps.officer.urls')),
    path('notice/', include('apps.notice.urls')),
    path('gallery/', include('apps.gallery.urls')),
]

app_name = 'core'
urlpatterns = (
    [
        path('admin/', admin.site.urls),
    ]
    + urlpatterns_apps
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)