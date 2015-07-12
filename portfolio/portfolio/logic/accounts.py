from portfolio.models.photos import Album
from portfolio.models.portfolios import Portfolio


def set_default_user_related_data(form):
    """ Method that creates a default album, and a user related portfolio when registering a user """
    user = form.save()
    album = Album(name='Default', owner=user)
    album.save()
    portfolio = Portfolio(owner=user)
    portfolio.save()
