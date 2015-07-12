from django.contrib.auth.models import User
from django.db import models

from portfolio.models.photos import Photo


class Portfolio(models.Model):
    owner = models.OneToOneField(User, primary_key=True)
    description = models.CharField(max_length=300)
    photo = models.OneToOneField(Photo, null=True, blank=True)
