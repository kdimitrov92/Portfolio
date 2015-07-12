from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View

from portfolio.models.photos import Photo, Album
from portfolio.views.base import AuthenticatedView


class AllAlbumsView(View):
    """ View for displaying all albums of a provided user """
    TEMPLATE = 'album_all.html'

    def get(self, request, username):
        albums = Album.objects.filter(owner__username=username)

        context = {
            'albums': [album for album in albums],
        }

        return render(request, self.TEMPLATE, context)


class SingleAlbumView(View):
    """ View for displaying the contents of a given single album """
    TEMPLATE = 'album_view.html'

    def get(self, request, album_id):
        photos = Photo.objects.filter(album__id=album_id)

        context = {
            'photos': [photo for photo in photos if not photo.original],
        }

        return render(request, self.TEMPLATE, context)


class RemoveAlbumView(AuthenticatedView):
    """ View that handles the deletion of an album """
    def get(self, request):
        try:
            album = Album.objects.get(id=request.GET.get('album_id', None), owner=request.user)
            album.clear()
            album.delete()

            return redirect('portfolio.album.view_all')
        except ObjectDoesNotExist:
            raise Http404


class CreateNewAlbumView(AuthenticatedView):
    """ View that handles the creation of an album """
    def post(self, request):
        album_name = request.POST.get('album_name', '')

        if not album_name or Album.objects.filter(owner=request.user, name=album_name).exists():
            return redirect(request.POST.get('previous_page', '/'))

        album = Album(name=album_name, owner=request.user)
        album.save()

        return redirect(request.POST.get('previous_page', '/'))
