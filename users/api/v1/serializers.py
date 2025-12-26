from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from ...constants import *
from ...models import User
from users.models import Following


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

    def get_following(self, author):
        req = self.context.get("request", None)

        if req is None or not req.user.is_authenticated:
            return False

        current_user = req.user

        is_following = Following.objects.filter(
            follower=current_user,
            followee=author,
        ).exists()

        return is_following


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


class UserUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        allow_blank=False,
        required=False,
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

    # lưu user vào db
    # instance: user hiện tại
    # validated_data: dữ liệu input đã được validate
    def update(self, instance, validated_data):
        is_changed = False

        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            is_changed = True

        if "bio" in validated_data:
            instance.bio = validated_data["bio"]
            is_changed = True

        if "image" in validated_data:
            instance.image = validated_data["image"]
            is_changed = True

        if is_changed:
            instance.save()
            return instance

        return instance
