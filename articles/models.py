from django.db import models
from core.models import CoreModel
import articles.constants as constants


class Article(CoreModel):
    title = models.CharField(max_length=constants.TITLE_MAX_LENGTH)
    slug = models.CharField(max_length=constants.SLUG_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=constants.DESCRIPTION_MAX_LENGTH)
    body = models.TextField()
    status = models.SmallIntegerField(choices=constants.STATUS_CHOICES, default=constants.STATUS_DRAFT)
    author = models.ForeignKey(
        "users.User",
        related_name="articles",
        on_delete=models.RESTRICT,
        db_column="author_id",
        null=True,
    )
    favorites = models.ManyToManyField(
        "users.User",
        related_name="favorite_articles",
        db_table="favorite_articles",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="article_tags",
        db_table="article_tags",
    )

    class Meta:
        db_table = "articles"
