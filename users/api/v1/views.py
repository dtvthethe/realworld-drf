from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from users.models import Following, User
from core.permissions import IsNotOwner
from .serializers import (
    CurrentUserResponseSerializer,
    UserRegisterSerializer,
    ProfileResponseSerializer,
    UserLoginResponseSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
)


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        try:
            # lấy data từ request
            # dùng .get() để tránh lỗi "user" không tồn tại
            user_data = request.data.get("user", {})

            # sử dụng serializer để validate và lưu data
            serializer = self.get_serializer(data=user_data)

            # nếu data không hợp lệ, raise exception
            serializer.is_valid(raise_exception=True)

            # gọi serializer.create() để lưu user vào db
            user = serializer.save()

            response_data = UserRegisterSerializer(user).data

            return Response({"user": response_data}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )

    # detail=False: ko làm việc với 1 object, không cần pk để xác định là user nào
    # detail=True: làm việc với 1 object cụ thể, cần có pk: /api/v1/users/12/login/
    @action(methods=["POST"], detail=False, url_path="login")
    def login(self, request):
        try:
            auth_data = request.data.get("user", {})
            # gọi riêng serializer để validate dữ liệu đăng nhập ko dùng self.get_serializer() của class
            serializer = UserLoginSerializer(data=auth_data)
            serializer.is_valid(raise_exception=True)

            # lấy object dict user đã được xác thực (đã chạy hàm validate() trong serializer)
            user_dict = serializer.validated_data
            response_data = UserLoginResponseSerializer(user_dict).data

            return Response({"user": response_data}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )


class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()
    # mạc định là id, đổi sang username
    lookup_field = "username"

    def retrieve(self, request, username=None):
        try:
            user = self.get_queryset().get(username=username)
            response_serializer = ProfileResponseSerializer(user)

            return Response({"profile": response_serializer.data}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsNotOwner],
    )
    def follow(self, request, username=None):
        try:
            user_want_to_follow = self.get_object()  # kích hoạt hàm get_object()
            current_user = request.user

            # follow user
            Following.objects.get_or_create(
                follower=current_user,
                followee=user_want_to_follow,
            )
            serializer_response = ProfileResponseSerializer(user_want_to_follow)

            return Response({"profile": serializer_response.data}, status=HTTP_200_OK)
        except Http404:
            return Response({"error": "Article not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[IsAuthenticated, IsNotOwner],
    )
    def unfollow(self, request, username=None):
        try:
            user_want_to_unfollow = self.get_object()
            current_user = request.user

            # unfollow user
            # case ko ko tồn tại thì ko lỗi
            Following.objects.filter(
                follower=current_user,
                followee=user_want_to_unfollow,
            ).delete()
            serializer_response = ProfileResponseSerializer(user_want_to_unfollow)

            return Response({"profile": serializer_response.data}, status=HTTP_200_OK)
        except Http404:
            return Response({"error": "Article not found."}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )


class CurrentUserViewSet(GenericViewSet):
    # chỉ có thể truy cập khi có token, nếu không có cái này thì ai cũng có thể  truy cập
    # cái này ko trực tiếp verify token mà nhờ JWTAuthentication trong settings.py
    # Authorization: Bearer <access_token>
    permission_classes = [IsAuthenticated]

    # vì ko có pk nên phải khai báo riêng trong urls.py
    def retrieve(self, request):
        try:
            user = request.user
            response_data = CurrentUserResponseSerializer(user).data

            return Response({"user": response_data}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )

    # vì ko có pk nên phải khai báo riêng trong urls.py
    def update(self, request):
        try:
            user = request.user
            user_data = request.data.get("user", {})
            serializer = UserUpdateSerializer(
                user,
                data=user_data,
                partial=True,  # cho phép cập nhật 1 phần
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response_data = CurrentUserResponseSerializer(user).data

            return Response({"user": response_data}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": e.detail},
                status=HTTP_400_BAD_REQUEST,
            )
