from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from users.models import User
from .serializers import (
    UserRegisterSerializer,
    ProfileResponseSerializer,
    UserLoginResponseSerializer,
    UserLoginSerializer,
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
