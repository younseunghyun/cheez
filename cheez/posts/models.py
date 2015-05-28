from django.db import models
from users.models import User
from cheez.models import BaseModel


'''
#To get all sql queries sent by Django from py shell
import logging
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())
'''


class Post(BaseModel):
    deleted = models.BooleanField(default=False)
    image_url = models.URLField()
    like_count = models.IntegerField(default=0)
    link_click_count = models.IntegerField(default=0)
    reported_count = models.IntegerField(default=0)
    saved_count = models.IntegerField(default=0)
    source_url = models.URLField()
    subtitle = models.CharField(max_length=512, null=True)
    title = models.CharField(max_length=256)

    user = models.ForeignKey('users.User', related_name='writed_posts')

    read_users = models.ManyToManyField('users.User', through='ReadPostRel', related_name='read_posts')
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def add_tags(self, tag_names):

        for tag_name in set(tag_names):
            tag, created = Tag.objects.get_or_create(
                name=tag_name
            )
            self.tags.add(tag)

            if not created:
                tag.post_count += 1

            tag.save()


    def read_by(self, user_or_user_id, link_clicked=False, rating=0, saved=False):
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

        read_post, created = ReadPostRel.objects.get_or_create(
            post_id=self.id,
            user_id=user_id,
        )

        if link_clicked and (created or not read_post.link_clicked):
            self.link_click_count += 1
        if saved and (created or not read_post.saved):
            self.saved_count += 1

        self.save()

        read_post.link_clicked = link_clicked
        read_post.saved = saved
        read_post.rating = rating
        read_post.save()

    def __str__(self):
        return self.title

class Comment(BaseModel):
    comment = models.CharField(max_length=512)

    user = models.ForeignKey('users.User', related_name='comments')
    post = models.ForeignKey('Post', related_name='comments')

    def __str__(self):
        return self.comment


class Tag(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    post_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ReadPostRel(BaseModel):
    user = models.ForeignKey('users.User', related_name='read_post_rels')
    post = models.ForeignKey('Post', related_name='read_post_rels')

    link_clicked = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' ' + str(self.post)

    class Meta:
        unique_together = (('user', 'post',),)

class Report(BaseModel):
    user = models.ForeignKey('users.User')
    post = models.ForeignKey('posts.Post')
    reason = models.TextField()


