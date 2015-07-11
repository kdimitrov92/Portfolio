from django.conf.urls import patterns, url

from portfolio.views.home import HomeView
from portfolio.views.portfolios import OwnPortfolioView, PortfolioView
from portfolio.views.photos import\
    AddPhotoView, AllPhotosView, SinglePhotoView,\
    EditPhotoView, RemovePhotoView, AddAltPhotoView,\
    like_photo, CopyPhotoView, CreateNewAlbumView
from portfolio.views.comments import CommentPhotoView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='portfolio.home'),
    url(r'^portfolio$', OwnPortfolioView.as_view(), name='portfolio.portfolio'),

    url(r'^user/(?P<username>.+)$', PortfolioView.as_view(), name='portfolio.home'),

    # Not implemented
    url(r'^albums/all$', HomeView.as_view(), name='portfolio.album.view_all'),
    url(r'^albums/view/(?P<album_id>.+)$', HomeView.as_view(), name='portfolio.album.view'),
    url(r'^albums/add$', CreateNewAlbumView.as_view(), name='portfolio.album.add'),

    url(r'^photos/view/(?P<photo_id>.+)$', SinglePhotoView.as_view(), name='portfolio.photo.view'),
    url(r'^photos/like/(?P<photo_id>.+)', like_photo, name='portfolio.photo.like'),
    url(r'^photos/add$', AddPhotoView.as_view(), name='portfolio.photo.add'),
    url(r'^photos/edit', EditPhotoView.as_view(), name='portfolio.photo.edit'),
    url(r'^photos/remove', RemovePhotoView.as_view(), name='portfolio.photo.remove'),
    url(r'^photos/add-alt', AddAltPhotoView.as_view(), name='portfolio.photo.add-alt'),
    url(r'^photos/comment$', CommentPhotoView.as_view(), name='portfolio.photo.comment'),
    url(r'^photos/copy/(?P<photo_id>.+)$', CopyPhotoView.as_view(), name='portfolio.photo.copy'),

    # Not implemented
    url(r'^photos/all$', AllPhotosView.as_view(), name='portfolio.photo.all'),

)
