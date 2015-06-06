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


    def read_by(self, user_or_user_id, **kwargs):
        """

        :param user_or_user_id:
        :return: None
        """
        if isinstance(user_or_user_id, User):
            user_id = user_or_user_id.id
        elif type(user_or_user_id) == type(1):
            user_id = user_or_user_id
        else:
            raise TypeError('The first parameter must have type \'User\' or \'int\'')

        if isinstance(kwargs['post'], Post):
            post_id = kwargs['post'].id
        else:
            post_id = kwargs['post']



        read_post, created = ReadPostRel.objects.get_or_create(
            post_id=self.id,
            user_id=user_id,
        )

        liked = kwargs.get('liked')
        link_clicked = kwargs.get('link_clicked')
        saved = kwargs.get('saved')
        rating = kwargs.get('rating')

        view_started_time = int(kwargs.get('view_started_time'))
        view_ended_time = int(kwargs.get('view_ended_time'))
        link_opened_time = int(kwargs.get('link_opened_time'))
        link_closed_time = int(kwargs.get('link_closed_time'))

        if created:
            read_post.view_started_time = view_started_time
            read_post.view_ended_time = view_ended_time
            read_post.link_opened_time = link_opened_time
            read_post.link_closed_time = link_closed_time
        else:
            # 더 긴 시간으로 바꿈
            if (read_post.view_ended_time - read_post.view_started_time
                    < view_ended_time - view_started_time
                ):
                read_post.view_started_time = view_started_time
                read_post.view_ended_time = view_ended_time
            if (read_post.link_opened_time > 0 and
                    (read_post.link_closed_time - read_post.link_opened_time
                         < link_closed_time - link_opened_time)):
                read_post.link_opened_time = link_opened_time
                read_post.link_closed_time = link_closed_time

        if liked and (created or not read_post.liked):
            self.like_count += 1
        if link_clicked and (created or not read_post.link_clicked):
            self.link_click_count += 1
        if saved and (created or not read_post.saved):
            self.saved_count += 1

        self.save()

        read_post.liked = liked
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

    liked = models.BooleanField(default=False)
    link_clicked = models.BooleanField(default=False)

    # TODO : remove rating
    rating = models.IntegerField(default=0)
    saved = models.BooleanField(default=False)

    view_started_time = models.IntegerField(default=0)
    link_opened_time = models.IntegerField(default=0)
    link_closed_time = models.IntegerField(default=0)
    view_ended_time = models.IntegerField(default=0)


    def __str__(self):
        return str(self.user) + ' ' + str(self.post)

    class Meta:
        unique_together = (('user', 'post',),)

class Report(BaseModel):
    user = models.ForeignKey('users.User')
    post = models.ForeignKey('posts.Post')
    reason = models.TextField()


