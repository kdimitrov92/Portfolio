# import os

# from django.conf import settings

from portfolio.models.photos import Photo, Album


def add_photo(user, data):
    new_photo = Photo(
        name=data['name'],
        description=data['description'],
        owner=user,
        original=Photo.objects.filter(id=data['original']).first(),
        image=data['image'],
    )

    new_photo.save()

    album = Album.objects.filter(id=data['album']).first()

    if album:
        new_photo.album.add(album)

    if data['tags']:
        new_photo.tags.add(', '.join(data['tags']))

    new_photo.save()
    return new_photo.id
