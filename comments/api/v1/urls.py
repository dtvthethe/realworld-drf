from rest_framework.routers import SimpleRouter
from .views import CommentViewSet

router = SimpleRouter()
router.register(
    r"articles/(?P<slug>[^/.]+)/comments",
    CommentViewSet,
    basename="article-comments",
)

urlpatterns = router.urls
