from rest_framework import serializers
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
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            image=validated_data.get("image", ""),
        )
        return user


class ProfileResponseSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)
    following = serializers.SerializerMethodField()

    def get_following(self, obj):
        # TODO: implement following logic
        return False
