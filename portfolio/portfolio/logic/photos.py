from django.conf import settings

from portfolio.models.photos import Photo, Album


def add_photo(user, data):
    new_photo = Photo(
            name=data['name'],
            description=data['description'],
            owner=user,
            album=Album.objects.filter(id=data['album']).first(),
            original=Photo.objects.filter(id=data['original']).first(),
            image=data['image'],
            tags=data['tags']
        )

    new_photo.image.uplaod_to = settings.IMAGE_URL.format(user.username, data['album'])

    new_photo.save()
