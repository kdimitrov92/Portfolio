from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager


def get_img_url(instance, filename):
    return "{username}/{file}".format(username=instance.owner.username, file=filename)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, related_name='albums')


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='photos')
    album = models.ManyToManyField(Album, related_name='photos', blank=True)
    original = models.ForeignKey('self', related_name='alternative_versions', null=True, blank=True)
    image = models.ImageField(upload_to=get_img_url, null=False, blank=False)
    featured = models.BooleanField(default=False)
    liked = models.ManyToManyField(User, related_name='liked_by_set')
    tags = TaggableManager()
