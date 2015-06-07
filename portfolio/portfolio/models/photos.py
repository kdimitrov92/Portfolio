from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200)


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='photos')
    album = models.ManyToManyField(Album, related_name='photos', blank=True)
    original = models.ForeignKey('self', related_name='alternative_versions', blank=True)
    image = models.ImageField(null=False, blank=False)

    tags = TaggableManager()
