from django.db import models
from core.models import CoreModel
import tags.constants as constants


class Tag(CoreModel):
    name = models.CharField(max_length=constants.NAME_MAX_LENGTH, unique=True)
    class Meta:
        db_table = "tags"
