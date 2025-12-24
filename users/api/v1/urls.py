from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import CurrentUserViewSet, ProfileViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

# vì retrieve phải có pk nhưng current user thì không có pk
# nên phải khai báo riêng
user_detail = CurrentUserViewSet.as_view({
    "get": "retrieve"
})

urlpatterns = [
    *router.urls,
    path("user/", user_detail, name="current-user"), # /api/v1/user/
]
