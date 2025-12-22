from django.db import models
from core.models import CoreModel
import articles.constants as constants


class Article(CoreModel):
    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=constants.TITLE_MAX_LENGTH)
    slug = models.CharField(max_length=constants.SLUG_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=constants.DESCRIPTION_MAX_LENGTH)
    body = models.TextField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
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
