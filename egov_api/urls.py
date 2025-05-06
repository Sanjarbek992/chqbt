from django.urls import path, include

urlpatterns = [
    path("mygov/", include("egov_api.mygov.urls")),
    path("emaktab/", include("egov_api.emaktab.urls")),
]