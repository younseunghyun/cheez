from django.db import models


class UserPostRanking1(models.Model):
    user = models.ForeignKey('users.User')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    ranking = models.IntegerField(db_index=True)

    class Meta:
        unique_together = (('user', 'post',),)


class UserPostRanking2(models.Model):
    user = models.ForeignKey('users.User')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    ranking = models.IntegerField(db_index=True)

    class Meta:
        unique_together = (('user', 'post',),)

class PostRanking1(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    ranking = models.IntegerField(db_index=True)

class PostRanking2(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    ranking = models.IntegerField(db_index=True)

class CurrentTableNumber(models.Model):
    table_number = models.IntegerField(default=0)