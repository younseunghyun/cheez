from django.db import models
from cheez.models import BaseModel
from django.contrib.auth.models import (
    AbstractBaseUser,
)


class Device(BaseModel):
    device_id = models.CharField(max_length=512, unique=True)

    user = models.ForeignKey('User')

class SNSAccount(BaseModel):
    SNS_TYPE_FACEBOOK = 1
    SNS_TYPE_CHOICES = (
        (SNS_TYPE_FACEBOOK, 'FACEBOOK'),
    )

    sns_profile_url = models.URLField(null=True)
    sns_type = models.IntegerField(choices=SNS_TYPE_CHOICES, default=SNS_TYPE_FACEBOOK)
    sns_user_id = models.CharField(max_length=128)

    user = models.ForeignKey('User')

    class Meta:
        unique_together = ('sns_type', 'sns_user_id',)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=256, unique=True, null=True)

    USERNAME_FIELD = 'email'