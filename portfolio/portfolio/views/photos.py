from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View

from taggit.forms import TagField

from portfolio.logic.photos import \
    add_photo, get_single_photo_context,\
    get_all_photos, copy_photo, move_photo,\
    get_edit_photo_context, make_photo_changes
from portfolio.models.photos import Photo, Album
from portfolio.views.base import AuthenticatedView


class SinglePhotoView(View):
    """ View that shows all the information regarding a single photo """
    TEMPLATE = 'photo_view.html'

    def get(self, request, photo_id):
        return render(request, self.TEMPLATE, get_single_photo_context(request, photo_id))


class AllPhotosView(View):
    """ View that displays all original (non-alternative-version) photos uploaded by a given user """
    TEMPLATE = 'photo_all.html'

    def get(self, request, username):
        return render(request, self.TEMPLATE, get_all_photos(username))


class AddPhotoView(AuthenticatedView):
    """ View that handles the creation of a photo """
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
    """ View that handles the additiong of a photo in another album """
    def post(self, request, photo_id):
        copy_photo(request, photo_id)
        return redirect(request.POST.get('previous_page', '/'))


class MovePhotoView(AuthenticatedView):
    """ View that handles the transferring of a photofrom one photo album to another """
    def post(self, request):
        move_photo(request)
        return redirect(request.POST.get('previous_page', '/'))


class RemovePhotoView(AuthenticatedView):
    """ Handles the deletion of a photo """
    def get(self, request):
        try:
            photo = Photo.objects.get(id=request.GET.get('photo_id', None), owner=request.user)
            photo.delete()

            return redirect('portfolio.photo.all', username=request.user.username)
        except ObjectDoesNotExist:
            raise Http404


@login_required
def like_photo(request, photo_id):
    """ A View Method that registers a like by a user """
    try:
        photo = Photo.objects.get(id=int(photo_id))
        if not request.user.liked_by_set.filter(id=photo.id).exists():
            photo.liked.add(request.user)

        return redirect('portfolio.photo.view', photo_id=photo_id)
    except ObjectDoesNotExist:
        raise Http404


class EditPhotoView(AuthenticatedView):
    """ View that handles the changing of a photos details """
    TEMPLATE = 'photo_edit.html'

    def get(self, request):
        context = get_edit_photo_context(request)
        context.update({'form': EditPhotoForm()})
        return render(request, self.TEMPLATE, context)

    def post(self, request):
        form = EditPhotoForm(request.POST)
        if form.is_valid():
            photo_id = form.cleaned_data.get('photo_id', 0)
            make_photo_changes(request, photo_id, form)
            return redirect('portfolio.photo.view', photo_id=photo_id)

        return render(request, self.TEMPLATE, {'form': form})


class EditPhotoForm(forms.Form):
    class Meta:
        fields = ['photo_id', 'name', 'description', 'tags']

    photo_id = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    tags = TagField()
    featured = forms.BooleanField(required=False)


class AddAltPhotoView(AuthenticatedView):
    """ View that handles the adding of an alternative version to a photo """
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


class RemovePhotoFromAlbumView(AuthenticatedView):
    """ View that handles the removal of a photo from a given album """
    def post(self, request, photo_id):
        album_name = request.POST.get('album_name', '')
        album = Album.objects.filter(owner=request.user, name=album_name).first()
        photo = Photo.objects.filter(pk=photo_id, owner=request.user).first()
        if not album or not photo:
            return redirect(request.POST.get('previous_page', '/'))

        photo.album.remove(album)

        return redirect(request.POST.get('previous_page', '/'))
