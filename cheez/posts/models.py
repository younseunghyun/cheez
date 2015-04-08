from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=512)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
