from rest_framework.routers import SimpleRouter
from .views import ProfileViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = router.urls
