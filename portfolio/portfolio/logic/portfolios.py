from portfolio.models.portfolios import Portfolio
from portfolio.models.photos import Album, Photo
from portfolio.models.blogs import Blog


def get_portfolio_context(user):
    """ Get all the required information regarding a users portfolio """
    return {
        'portfolio': Portfolio.objects.get(owner=user),
        'albums': Album.objects.filter(owner=user),
        'featured_photos': Photo.objects.filter(owner=user, featured=True),
        'newest_photos': Photo.objects.filter(owner=user).order_by('-date_created')[:5],
        'newest_blogs': Blog.objects.filter(owner=user).order_by('-date_created')[:5],
    }
