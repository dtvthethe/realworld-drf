from django.db import models
from core.models import CoreModel


class Comment(CoreModel):
    body = models.TextField()
    article = models.ForeignKey(
        "articles.Article",
        related_name="comments",
        on_delete=models.CASCADE,
        db_column="article_id",
        null=True,
    )
    author = models.ForeignKey(
        "users.User",
        related_name="comments",
        on_delete=models.RESTRICT,
        db_column="author_id",
        null=True,
    )

    class Meta:
        db_table = "comments"
