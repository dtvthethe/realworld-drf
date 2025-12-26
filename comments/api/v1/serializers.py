from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.api.v1.serializers import ProfileResponseSerializer
from ...constants import *
from ...models import Comment


class CreateCommentSerializer(serializers.Serializer):
    body = serializers.CharField(
        min_length=BODY_MIN_LENGTH, allow_blank=False, required=True
    )

    def create(self, validated_data):
        req = self.context.get("request", None)
        article = self.context.get("article", None)

        if article is None:
            raise ValidationError("Request or Article context is missing.")

        comment = Comment.objects.create(
            body=validated_data.get("body"),
            article=article,
            author=req.user,
        )

        return comment


# sử dụng ModelSerializer để tự động map các trường với model
class ResponseCommentSerializer(serializers.ModelSerializer):
    author = ProfileResponseSerializer(read_only=True)

    # cách đặt lại tên trường
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "createdAt", "updatedAt", "body", "author"]
