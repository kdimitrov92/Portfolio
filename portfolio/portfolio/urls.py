from django.conf.urls import patterns, url

from portfolio.views.home import HomeView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='portfolio.home'),
)
