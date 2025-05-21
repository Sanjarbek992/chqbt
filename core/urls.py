from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CHQBT API",
        default_version='v1',
        description="Milliy tizim uchun API hujjat",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # OAuth2 token URL (POST /o/token/ → access_token, refresh_token)
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Swagger va Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Internationalized routes
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path(_('api/users/'), include('users.urls')),
)

# Media fayllar uchun
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
