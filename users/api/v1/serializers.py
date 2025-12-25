from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from ...constants import *
from ...models import User


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        allow_blank=False,
        required=True,
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        allow_blank=False,
        required=True,
    )
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        allow_blank=False,
        required=True,
        write_only=True,
    )
    bio = serializers.CharField(
        max_length=BIO_MAX_LENGTH,
        allow_blank=True,
        required=False,
    )
    image = serializers.URLField(
        max_length=IMAGE_MAX_LENGTH,
        allow_blank=True,
        required=False,
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken")
        return value

    # lưu user vào db
    def create(self, validated_data):
        # tạo object User
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            # password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            image=validated_data.get("image", ""),
        )
        # mã hóa password
        user.set_password(validated_data["password"])
        # lưu user vào db
        user.save()

        return user


class ProfileResponseSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)
    following = serializers.SerializerMethodField()

    def get_following(self, obj):
        # TODO: implement following logic
        return False


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        allow_blank=False,
        required=True,
    )
    password = serializers.CharField(
        allow_blank=False,
        required=True,
        write_only=True,
    )

    def validate(self, data):
        email = data.get("email", "")
        pwd = data.get("password", "")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError({"email": "Email not found"})

        if not user.check_password(pwd):
            raise serializers.ValidationError({"password": "Password is incorrect"})

        # tạo token và refresh token
        refresh = RefreshToken.for_user(user)

        # lấy access token
        token = str(refresh.access_token)

        # lấy refresh token
        refresh_token = str(refresh)

        return {
            "email": user.email,
            "username": user.username,
            "bio": user.bio,
            "image": user.image,
            "token": token,
            "refresh_token": refresh_token,
        }


class CurrentUserResponseSerializer(serializers.Serializer):
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)


class UserLoginResponseSerializer(CurrentUserResponseSerializer):
    token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
