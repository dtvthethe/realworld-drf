from django.db import models
from core.models import CoreModel


class Comment(CoreModel):
    body = models.TextField()

    class Meta:
        db_table = "comments"
