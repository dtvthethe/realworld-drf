from django.db import models
from core.models import CoreModel


class Tag(CoreModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "tags"
