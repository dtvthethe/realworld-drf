from django.db import models
from core.models import CoreModel
import articles.constants as constants


class Article(CoreModel):
    title = models.CharField(max_length=constants.TITLE_MAX_LENGTH)
    slug = models.CharField(max_length=constants.SLUG_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=constants.DESCRIPTION_MAX_LENGTH)
    body = models.TextField()
    status = models.SmallIntegerField(default=1)  # 1: Draft, 2: Published
    author = models.ForeignKey(
        "users.User",
        related_name="articles",
        on_delete=models.CASCADE,
        db_column="author_id",
        null=True,
    )
    favorites = models.ManyToManyField(
        "users.User",
        related_name="favorite_articles",
        null=True,
        db_table="favorite_articles",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="article_tags",
        null=True,
        db_table="article_tags",
    )

    class Meta:
        db_table = "articles"
