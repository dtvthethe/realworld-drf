from rest_framework.routers import SimpleRouter
from .views import TagViewSet

router = SimpleRouter()
router.register("tags", TagViewSet, basename="tags")

urlpatterns = router.urls
