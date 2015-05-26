from django.db import models
from cheez.models import BaseModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    def create(self, **kwargs):
        user = User()
        if 'email' in kwargs:
            user.email = UserManager.normalize_email(kwargs['email'])

        if 'name' in kwargs:
            user.name = kwargs['name']

        if 'password' in kwargs:
            user.set_password(kwargs['password'])

        return user

    def create_superuser(self, **kwargs):
        user = self.create(**kwargs)
        user.is_superuser = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=126, unique=True, null=True)
    name = models.CharField(max_length=128, null=True)

    profile_image = models.ImageField(upload_to='images/users/profile', null=True, blank=True)
    upload_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def get_full_name(self):
        return '{} ({})'.format(self.name, self.email)

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.get_full_name()


class Device(BaseModel):
    OS_TYPE_ANDROID, OS_TYPE_IOS = 1, 2
    OS_TYPE_CHOICES = (
        (OS_TYPE_ANDROID, 'ANDROID'),
        (OS_TYPE_IOS, 'IOS')
    )
    device_id = models.CharField(max_length=128)
    os_type = models.IntegerField(choices=OS_TYPE_CHOICES, default=OS_TYPE_ANDROID)
    os_version = models.CharField(max_length=64, null=True)

    # 사실상 null 불가능하나, 데이터 입력 용이하기 위해 null 가능하도록 설정해둠
    user = models.ForeignKey('User', related_name='devices', null=True)

    class Meta:
        unique_together = ('os_type', 'device_id', )


class SNSAccount(BaseModel):
    SNS_TYPE_FACEBOOK = 1
    SNS_TYPE_CHOICES = (
        (SNS_TYPE_FACEBOOK, 'FACEBOOK'),
    )

    sns_profile_url = models.URLField(null=True)
    sns_type = models.IntegerField(choices=SNS_TYPE_CHOICES, default=SNS_TYPE_FACEBOOK)
    sns_user_id = models.CharField(max_length=128)

    user = models.ForeignKey('User', related_name='sns_accounts', null=True)

    class Meta:
        unique_together = ('sns_type', 'sns_user_id',)


