from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View

from taggit.forms import TagField

from portfolio.logic.photos import add_photo
from portfolio.models.comments import PhotoComment
from portfolio.models.photos import Photo, Album
from portfolio.views.base import AuthenticatedView


class SinglePhotoView(View):
    TEMPLATE = 'photo_view.html'

    def get(self, request, photo_id):
        try:
            photo = Photo.objects.select_related('owner').select_related('album').get(id=photo_id)
        except ObjectDoesNotExist:
            raise Http404

        context = {
            'photo': photo,
            'liked': request.user.liked_by_set.filter(id=photo.id).exists(),
            'likes': photo.liked.count(),
            'alt_versions': Photo.objects.filter(original=photo),
            'comments': PhotoComment.objects.filter(photo=photo).order_by('-date_created').select_related('owner'),
        }

        return render(request, self.TEMPLATE, context)


class AllPhotosView(View):
    TEMPLATE = 'all_photos.html'

    def get(self, request, username):
        photos = Photo.objects.filter(owner__username=username)

        context = {
            'photo': [photo for photo in photos if not photo.original],
        }

        return render(request, self.TEMPLATE, context)


class AddPhotoView(AuthenticatedView):
    TEMPLATE = 'photo_add.html'

    def get(self, request):
        context = {
            'form': AddPhotoForm(),
            'original': request.GET.get('original', None),
            'albums': Album.objects.filter(owner__username=request.user.username).select_related('owner'),
        }

        return render(request, self.TEMPLATE, context)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = add_photo(request.user, form.cleaned_data)
        else:
            return render(request, self.TEMPLATE, {'form': form})

        return redirect('portfolio.photo.view', photo_id=photo)


class AddPhotoForm(forms.Form):
    class Meta:
        fields = ['name', 'description', 'image', 'album', 'original', 'tags']

    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=True)
    album = forms.IntegerField(required=False)
    original = forms.IntegerField(required=False)
    tags = TagField()


class CopyPhotoView(AuthenticatedView):
    TEMPLATE = 'copy_photo.html'

    def post(self, request, photo_id):
        try:
            print 100 * '-'
            photo = Photo.objects.get(id=photo_id, owner=request.user)
            print 100 * '-'
            print request.POST
            album = Album.objects.get(name=request.POST.get('album_name', 'Default'), owner=request.user)
            print 100 * '-'
            print photo.album.all()
            photo.album.add(album)
            print request.POST.get('album_name', 'Default')
            print photo.album.all()
            print 100 * '-'
            # photo.save()
            print 100 * '-'
            return redirect(request.POST.get('previous_page', '/'))
        except ObjectDoesNotExist:
            raise Http404


class MovePhotoView(AuthenticatedView):
    TEMPLATE = 'move_photo.html'

    def post(self, request):
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


class RemovePhotoView(AuthenticatedView):
    TEMPLATE = 'remove_photo.html'

    def get(self, request):
        try:
            photo = Photo.objects.get(id=request.GET.get('photo_id', None), owner=request.user)
            photo.delete()

            return redirect('portfolio.photo.all')
        except ObjectDoesNotExist:
            raise Http404


@login_required
def like_photo(request, photo_id):
    try:
        photo = Photo.objects.get(id=int(photo_id))
        if not request.user.liked_by_set.filter(id=photo.id).exists():
            photo.liked.add(request.user)

        return redirect('portfolio.photo.view', photo_id=photo_id)
    except ObjectDoesNotExist:
        raise Http404


class EditPhotoView(AuthenticatedView):
    TEMPLATE = 'photo_edit.html'

    def get(self, request):
        try:
            photo_id = int(request.GET.get('photo_id', 0))
            photo = Photo.objects.select_related('album').get(id=photo_id, owner=request.user)
        except ObjectDoesNotExist:
            raise Http404

        context = {
            'albums': Album.objects.filter(owner=request.user),
            'photo': photo,
            'form': EditPhotoForm(),
        }

        return render(request, self.TEMPLATE, context)

    def post(self, request):
        form = EditPhotoForm(request.POST)
        if form.is_valid():
            try:
                photo_id = form.cleaned_data.get('photo_id', 0)
                photo = Photo.objects.get(id=photo_id, owner=request.user)
            except ObjectDoesNotExist:
                raise Http404

            photo.name = form.cleaned_data['name']
            photo.description = form.cleaned_data['description']
            photo.tags.set(', '.join(form.cleaned_data['tags']))

            photo.save()

            return redirect('portfolio.photo.view', photo_id=photo.id)

        return render(request, self.TEMPLATE, {'form': form})


class EditPhotoForm(forms.Form):
    class Meta:
        fields = ['photo_id', 'name', 'description', 'tags']

    photo_id = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    tags = TagField()


class AddAltPhotoView(AuthenticatedView):
    TEMPLATE = 'photo_add.html'

    def get(self, request):
        context = {
            'form': AddPhotoForm(),
            'original': request.GET.get('original', None),
            'albums': Album.objects.filter(owner__username=request.user.username).select_related('owner'),
        }

        return render(request, self.TEMPLATE, context)

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = add_photo(request.user, form.cleaned_data)
        else:
            return render(request, self.TEMPLATE, {'form': form})

        return redirect('portfolio.photo.view', photo_id=photo)


class CreateNewAlbumView(AuthenticatedView):
    def post(self, request):
        album_name = request.POST.get('album_name', '')
        if Album.objects.filter(owner=request.user, name=album_name).exists():
            return redirect(request.POST.get('previous_page', '/'))

        album = Album(name=album_name, owner=request.user)
        album.save()

        print 100 * '-'
        print request.POST.get('previous_page', '/')
        return redirect(request.POST.get('previous_page', '/'))
