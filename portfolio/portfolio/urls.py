from django.conf.urls import patterns, url

from portfolio.views.home import HomeView
from portfolio.views.portfolios import OwnPortfolioView, PortfolioView
from portfolio.views.photos import\
    AddPhotoView, AllPhotosView, SinglePhotoView,\
    EditPhotoView, RemovePhotoView, AddAltPhotoView,\
    like_photo, CopyPhotoView,\
    RemovePhotoFromAlbumView
from portfolio.views.comments import CommentPhotoView
from portfolio.views.albums import AllAlbumsView, SingleAlbumView, RemoveAlbumView, CreateNewAlbumView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='portfolio.home'),
    url(r'^portfolio$', OwnPortfolioView.as_view(), name='portfolio.portfolio'),

    url(r'^user/(?P<username>.+)$', PortfolioView.as_view(), name='portfolio.home'),

    url(r'^albums/all/(?P<username>.+)$', AllAlbumsView.as_view(), name='portfolio.album.view_all'),
    url(r'^albums/view/(?P<album_id>.+)$', SingleAlbumView.as_view(), name='portfolio.album.view'),
    url(r'^albums/add$', CreateNewAlbumView.as_view(), name='portfolio.album.add'),
    url(r'^albums/remove$', RemoveAlbumView.as_view(), name='portfolio.album.remove'),

    url(r'^photos/view/(?P<photo_id>.+)$', SinglePhotoView.as_view(), name='portfolio.photo.view'),
    url(r'^photos/like/(?P<photo_id>.+)', like_photo, name='portfolio.photo.like'),
    url(r'^photos/add$', AddPhotoView.as_view(), name='portfolio.photo.add'),
    url(r'^photos/edit', EditPhotoView.as_view(), name='portfolio.photo.edit'),
    url(r'^photos/remove-from-album/(?P<photo_id>.+)$', RemovePhotoFromAlbumView.as_view(),
        name='portfolio.photo.remove-from-album'),
    url(r'^photos/remove', RemovePhotoView.as_view(), name='portfolio.photo.remove'),
    url(r'^photos/add-alt', AddAltPhotoView.as_view(), name='portfolio.photo.add-alt'),
    url(r'^photos/comment$', CommentPhotoView.as_view(), name='portfolio.photo.comment'),
    url(r'^photos/copy/(?P<photo_id>.+)$', CopyPhotoView.as_view(), name='portfolio.photo.copy'),
    url(r'^photos/all/(?P<username>.+)$', AllPhotosView.as_view(), name='portfolio.photo.all'),

)
