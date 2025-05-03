from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, DistrictViewSet, SchoolViewSet

router = DefaultRouter()
router.register('regions', RegionViewSet, basename='region')
router.register('districts', DistrictViewSet, basename='district')
router.register('schools', SchoolViewSet, basename='school')

urlpatterns = router.urls