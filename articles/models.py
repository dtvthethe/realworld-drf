from django.db import models
from core.models import CoreModel
import articles.constants as constants


class Article(CoreModel):
    title = models.CharField(max_length=constants.TITLE_MAX_LENGTH)
    slug = models.CharField(max_length=constants.SLUG_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=constants.DESCRIPTION_MAX_LENGTH)
    body = models.TextField()

    class Meta:
        db_table = "articles"
