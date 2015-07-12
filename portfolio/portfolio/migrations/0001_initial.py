# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import portfolio.models.photos
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=120)),
                ('blog', models.ForeignKey(related_name='commented_blog', to='portfolio.Blog')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=portfolio.models.photos.get_img_url)),
                ('featured', models.BooleanField(default=False)),
                ('album', models.ManyToManyField(related_name='photos', to='portfolio.Album', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('owner', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(max_length=300)),
                ('photo', models.OneToOneField(null=True, blank=True, to='portfolio.Photo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photocomment',
            name='owner',
            field=models.ForeignKey(related_name='comment_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photocomment',
            name='photo',
            field=models.ForeignKey(related_name='commented_photo', to='portfolio.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='liked',
            field=models.ManyToManyField(related_name='liked_by_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='original',
            field=models.ForeignKey(related_name='alternative_versions', blank=True, to='portfolio.Photo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(related_name='photos', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='owner',
            field=models.ForeignKey(related_name='comment_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(related_name='photo_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(related_name='albums', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
