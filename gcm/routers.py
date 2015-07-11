from rest_framework.routers import DefaultRouter

from gcm.api import DevicesViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'devices', DevicesViewSet)

urlpatterns = router.urls
