from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from users.models import User
from .serializers import UserRegisterSerializer, ProfileResponseSerializer


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
                {"errors": str(e)},
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
                {"errors": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )
