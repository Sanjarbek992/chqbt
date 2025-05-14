from django.urls import path, include
from mygov.views import FakeMygovAPIView
urlpatterns = [
    path("mygov/", include("egov_api.mygov.urls")),
    path("emaktab/", include("egov_api.emaktab.urls")),
    path('fake-child-info/', FakeMygovAPIView.as_view(), name='fake-child-info'),
]