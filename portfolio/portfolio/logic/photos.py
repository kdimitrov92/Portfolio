from portfolio.models.photos import Photo, Album
from portfolio.models.comments import PhotoComment
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def add_photo(user, data):
    """ Creates a photo by the given user, with the given speicification in data """
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


def get_single_photo_context(request, photo_id):
    """ Acquires the information for a single photo called by the photos ID """
    try:
        photo = Photo.objects.select_related('owner').select_related('album').get(id=photo_id)
    except ObjectDoesNotExist:
        raise Http404

    return {
        'photo': photo,
        'liked': request.user.liked_by_set.filter(id=photo.id).exists(),
        'likes': photo.liked.count(),
        'alt_versions': Photo.objects.filter(original=photo),
        'comments': PhotoComment.objects.filter(photo=photo).order_by('-date_created').select_related('owner'),
    }


def get_all_photos(username):
    """ Get all photos posted by given user """
    photos = Photo.objects.filter(owner__username=username)

    return {
        'photos': [photo for photo in photos if not photo.original],
    }


def copy_photo(request, photo_id):
    """ Copy photo to a given album """
    try:
        photo = Photo.objects.get(id=photo_id, owner=request.user)
        album = Album.objects.get(name=request.POST.get('album_name', 'Default'), owner=request.user)

        photo.album.add(album)
    except ObjectDoesNotExist:
        raise Http404


def move_photo(request):
    """ Move a photo from one album to another """
    try:
        photo = Photo.objects.get(id=request.GET.get('photo_id', None))
        to_album = Album.objects.get(id=request.GET.get('to_album_id', None))
        from_album = Album.objects.get(id=request.GET.get('from_album_id', None))

        if request.user != photo.onwer or request.user != from_album.owner or request.user != to_album.owner:
            raise Http404

        photo.album.remove(from_album)
        photo.album.add(to_album)
        photo.save()
    except ObjectDoesNotExist:
        raise Http404


def get_edit_photo_context(request):
    """ Get the information for a single photo that is required for editting """
    try:
        photo_id = int(request.GET.get('photo_id', 0))
        photo = Photo.objects.select_related('album').get(id=photo_id, owner=request.user)
    except ObjectDoesNotExist:
        raise Http404

    return {
        'albums': Album.objects.filter(owner=request.user),
        'photo': photo,
    }


def make_photo_changes(request, photo_id, form):
    """ Apply the changes made via an edit form to a given photo """
    try:
        photo = Photo.objects.get(id=photo_id, owner=request.user)
    except ObjectDoesNotExist:
        raise Http404

    photo.name = form.cleaned_data['name']
    photo.description = form.cleaned_data['description']
    photo.tags.set(', '.join(form.cleaned_data['tags']))
    photo.featured = form.cleaned_data['featured']
    photo.save()
