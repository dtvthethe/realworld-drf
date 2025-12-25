from django.db import models
from django.db.models import Q, F
from core.models import CoreModel
import users.constants as constants
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class User(CoreModel, AbstractUser):
    # xem: AbstractUser
    # username = models.CharField(max_length=constants.USERNAME_MAX_LENGTH, unique=True)

    # email có trong AbstractUser, override để  unique
    email = models.EmailField(max_length=constants.EMAIL_MAX_LENGTH, unique=True)

    # TODO: bỏ first_name và last_name từ AbstractUser
    # first_name = models.CharField(max_length=150, blank=True, null=True)
    # last_name = models.CharField(max_length=150, blank=True, null=True)

    # xem: AbstractBaseUser
    # password = models.CharField(max_length=constants.PASSWORD_MAX_LENGTH)

    bio = models.CharField(max_length=constants.BIO_MAX_LENGTH, null=True)
    image = models.CharField(max_length=constants.IMAGE_MAX_LENGTH, null=True)

    # dùng email để login thay vì username
    USERNAME_FIELD = "email"

    # trong AbstractUser set cột email là required, nhưng email đã là USERNAME_FIELD nên được tự động coi là required
    REQUIRED_FIELDS = []

    # xem: AbstractBaseUser
    # mã hóa password
    # def set_password(self, input):
    #     self.password = make_password(input)

    # xem: AbstractBaseUser
    # kiểm tra password đúng hay không
    # def check_password(self, input):
    #     return check_password(input, self.password)

    # ko dùng cái này thay bằng Following model bên dưới
    # user.following.all()   # mình follow ng khác
    # user.followers.all()   # ng khác follow mình
    # following = models.ManyToManyField(
    #     "self",
    #     symmetrical=False, # A follow B khác B follow A
    #     related_name="followers",
    #     null=True,
    #     db_table="user_followers",
    # )

    class Meta:
        db_table = "users"


# TODO: chưa hiểu lắm, khi code cần tìm hiểu thêm
class Following(models.Model):
    """
    ### follow
    Following.objects.create(
        follower=request.user,
        followee=target_user
    )

    ### unfollow
    Following.objects.filter(
        follower=request.user,
        followee=target_user
    ).delete()

    ### mình đang follow ai
    user.following.select_related("followee")

    ### ai follow mình
    user.followers.select_related("follower")

    ### check đã follow chưa
    Following.objects.filter(
        follower=request.user,
        followee=target_user
    ).exists()
    """

    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        db_column="follower_id",
    )
    followee = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
        db_column="followee_id",
    )

    class Meta:
        db_table = "user_followers"
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followee"],
                name="unique_follow_relation",
            ),
            models.CheckConstraint(
                condition=~Q(follower=F("followee")),
                name="prevent_self_follow",
            ),
        ]
