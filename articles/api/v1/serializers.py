from rest_framework import serializers
from django.utils.text import slugify
from ...constants import *
from ...models import Article


class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=TITLE_MAX_LENGTH,
        min_length=TITLE_MIN_LENGTH,
        allow_blank=False,
        required=True,
    )
    description = serializers.CharField(
        max_length=DESCRIPTION_MAX_LENGTH,
        min_length=DESCRIPTION_MIN_LENGTH,
        allow_blank=False,
        required=True,
    )
    body = serializers.CharField(
        min_length=BODY_MIN_LENGTH, allow_blank=False, required=True
    )
    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )

    # TODO: save author
    # TODO: save neseted tags

    def create(self, validated_data):
        return Article.objects.create(
            slug=slugify(validated_data["title"]), **validated_data
        )


class ResponseArticleSerializer(serializers.Serializer):
    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)
    tagList = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_favorited(self, obj):
        # TODO: implement favorited
        return False

    def get_favoritesCount(self, obj):
        # TODO: implement favorited
        return 0

    def get_tagList(self, obj):
        # TODO: implement tags
        return []

    def get_author(self, obj):
        # TODO: implement author serialization
        return {}

    def get_createdAt(self, obj):
        return obj.created_at

    def get_updatedAt(self, obj):
        return obj.updated_at
