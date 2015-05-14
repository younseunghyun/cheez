from django.db import models
from cheez.models import BaseModel


class OG(BaseModel):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=1024, null=True)
    author = models.CharField(max_length=256, null=True)
    image = models.URLField(null=True)
    video = models.URLField(null=True)
    description = models.CharField(max_length=2048, null=True)