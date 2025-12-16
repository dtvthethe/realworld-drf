from django.db import models
from core.models import CoreModel
import users.constants as constants


class User(CoreModel):
    username = models.CharField(max_length=constants.USERNAME_MAX_LENGTH, unique=True)
    email = models.EmailField(max_length=constants.EMAIL_MAX_LENGTH, unique=True)
    password = models.CharField(max_length=constants.PASSWORD_MAX_LENGTH)
    bio = models.CharField(max_length=constants.BIO_MAX_LENGTH, null=True)
    image = models.CharField(max_length=constants.IMAGE_MAX_LENGTH, null=True)
    class Meta:
        db_table = "users"
