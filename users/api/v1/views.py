from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from users.models import User
from .serializers import UserRegisterSerializer


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
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

        return Response({"user": response_data})


class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()
    # mạc định là id, đổi sang username
    lookup_field = "username"

    def retrieve(self, request, username=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({"user": serializer.data})
