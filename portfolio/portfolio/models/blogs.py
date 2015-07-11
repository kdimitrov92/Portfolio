from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='photo_owner')
    date_created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
