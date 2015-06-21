from django.conf.urls import patterns, url

from portfolio.views.home import HomeView
from portfolio.views.portfolios import PortfolioView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='portfolio.home'),
    url(r'^portfolio$', PortfolioView.as_view(), name='portfolio.portfolio'),

    url(r'^albums/all$', HomeView.as_view(), name='portfolio.album.view_all'),
    url(r'^albums/view/(?P<album_id>.+)$', HomeView.as_view(), name='portfolio.album.view'),
    url(r'^albums/add$', HomeView.as_view(), name='portfolio.album.add'),

    url(r'^photos/view/(?P<photo_id>.+)$', HomeView.as_view(), name='portfolio.photo.view'),
    url(r'^photos/add$', HomeView.as_view(), name='portfolio.photo.add'),
)
