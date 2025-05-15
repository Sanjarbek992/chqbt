from django.urls import path, include
from egov_api.mygov.views import FakeMygovAPIView
urlpatterns = [
    path('fake-child-info/', FakeMygovAPIView.as_view(), name='fake-child-info'),
]