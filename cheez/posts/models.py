from django.db import models
from users.models import User
from cheez.models import BaseModel


class Post(models.Model):
    like_count = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)
    source_url = models.URLField()
    subtitle = models.CharField(max_length=512, null=True)
    title = models.CharField(max_length=256)

    user = models.ForeignKey('users.User', related_name='writed_posts')

    like_users = models.ManyToManyField('users.User', through='LikePostRel', related_name='like_posts')
    read_users = models.ManyToManyField('users.User', through='ReadPostRel', related_name='read_posts')

    def liked_by(self, user_or_user_id):
        """

        :param user_or_user_id: 해당 post를 좋아한 User 객체 또는 좋아한 User의 id
                                이외의 경우에는 TypeError 발생시킴
        :return: None
        """
        if isinstance(user_or_user_id, User):
            user_id = user_or_user_id.id
        elif type(user_or_user_id) == type(1):
            user_id = user_or_user_id
        else:
            raise TypeError('The first parameter must have type \'User\' or \'int\'')

        like_post, created = LikePostRel.objects.get_or_create(
            post_id=self.id,
            user_id=user_id,
        )
        like_post.like_type = LikePostRel.LIKE_TYPE_LIKE
        like_post.save()

        self.like_count += 1
        self.save()

    def read_by(self, user_or_user_id):
        """

        :param user_or_user_id: liked_by()와 동일
        :return: None
        """
        if isinstance(user_or_user_id, User):
            user_id = user_or_user_id.id
        elif type(user_or_user_id) == type(1):
            user_id = user_or_user_id
        else:
            raise TypeError('The first parameter must have type \'User\' or \'int\'')

        read_post = ReadPostRel(
            post_id=self.id,
            user_id=user_id,
        )
        read_post.save()

        self.read_count += 1
        self.save()

    def __str__(self):
        return self.title


class LikePostRel(BaseModel):
    LIKE_TYPE_HATE, LIKE_TYPE_PASS, LIKE_TYPE_LIKE = -1, 0, 1
    LIKE_TYPE_CHOICES = (
        (LIKE_TYPE_HATE, 'HATE'),
        (LIKE_TYPE_PASS, 'PASS'),
        (LIKE_TYPE_LIKE, 'LIKE'),
    )

    like_type = models.IntegerField(choices=LIKE_TYPE_CHOICES, default=LIKE_TYPE_PASS)

    user = models.ForeignKey('users.User', related_name='like_post_rels')
    post = models.ForeignKey('Post', related_name='like_post_rels')

    class Meta:
        unique_together = ('user', 'post',)


class ReadPostRel(BaseModel):
    user = models.ForeignKey('users.User', related_name='read_post_rels')
    post = models.ForeignKey('Post', related_name='read_post_rels')
