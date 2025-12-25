from rest_framework import serializers
from django.utils.text import slugify
from users.api.v1.serializers import ProfileResponseSerializer
from ...constants import *
from ...models import Article
from tags.models import Tag
from tags.constants import NAME_MAX_LENGTH


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
    tagList = serializers.ListField(
        child=serializers.CharField(max_length=NAME_MAX_LENGTH),
        allow_empty=True,
        required=False,
    )

    # 1 dấu `*`: convert sang kiểu tuple
    # 2 dấu `**`: convert sang kiểu dict
    def create(self, validated_data):
        tags = validated_data.pop("tagList", [])
        current_user = self.context["request"].user # lấy user từ context được truyền vào từ view
        article = Article.objects.create(
            slug=slugify(validated_data["title"]),
            author=current_user,
            **validated_data
        )

        for tag in tags:
            # get hoặc tạo mới tag nếu chưa tồn tại
            # trả về tuple
            tag = Tag.objects.get_or_create(name=tag)
            # thêm tag vào article, tự động lưu vào db bảng trung gian (article_tags)
            article.tags.add(tag[0])

        return article

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
    author = ProfileResponseSerializer(read_only=True)

    def get_favorited(self, article):
        # TODO: implement favorited
        return False

    def get_favoritesCount(self, article):
        # TODO: implement favorited
        return 0

    def get_tagList(self, article):
        # flat=False: <QuerySet [{'name': 'Django'}, {'name': 'Python'}...]>
        # flat=True: <QuerySet ['Django', 'Python'...]>
        tags = article.tags.all().values_list("name", flat=True)
        return list(tags)

    def get_createdAt(self, article):
        return article.created_at

    def get_updatedAt(self, article):
        return article.updated_at
