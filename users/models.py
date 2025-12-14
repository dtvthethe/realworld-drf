from django.db import models
from core.models import CoreModel


class User(CoreModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(max_length=255)
    bio = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "users"
