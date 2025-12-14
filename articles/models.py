from django.db import models
from core.models import CoreModel


class Article(CoreModel):
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        db_table = "articles"
