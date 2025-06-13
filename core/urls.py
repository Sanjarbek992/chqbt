from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]

urlpatterns += [
    path(_("api/users/"), include("users.urls")),
    path(_("api/materials/"), include("material_base.urls")),
    path(_("api/egov_api/"), include("egov_api.urls")),
    path(_("api/lesson/"), include("lesson.urls")),
    path(_("api/training/"), include("training.urls")),
    path(_("api/competition/"), include("competition.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
