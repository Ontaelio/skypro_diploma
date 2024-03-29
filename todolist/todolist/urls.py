from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import core.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'))),
    path("goals/", include(("goals.urls", 'goals'))),

    path('bot/connect', core.views.TgUserConnectView.as_view(), name='create_tg_user'),
    path('bot/verify', core.views.TgUserVerifyView.as_view(), name='verify_tg_user'),
    path('bot/delete/<int:tg_user>', core.views.TgUserDeleteView.as_view(), name='delete_binding'),

    path('oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += [
        # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        path('api-auth/', include('rest_framework.urls')),
    ]
