from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path("goals/", include("goals.urls")),

    path('oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += [
        # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        path('api-auth/', include('rest_framework.urls')),
    ]
