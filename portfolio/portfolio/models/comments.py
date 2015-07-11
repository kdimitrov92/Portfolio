from django.contrib.auth.models import User
from django.db import models

from portfolio.models.photos import Photo
from portfolio.models.blogs import Blog


class Comment(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=120)
    owner = models.ForeignKey(User, related_name='comment_owner')


class PhotoComment(Comment):
    photo = models.ForeignKey(Photo, related_name='commented_photo')


class BlogComment(Comment):
    blog = models.ForeignKey(Blog, related_name='commented_blog')
