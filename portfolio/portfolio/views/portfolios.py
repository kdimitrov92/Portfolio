from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View

from portfolio.models.portfolios import Portfolio
from portfolio.models.photos import Album, Photo
from portfolio.models.blogs import Blog

from portfolio.views.base import AuthenticatedView


def get_portfolio_context(user):
    return {
        'portfolio': Portfolio.objects.get(owner=user),
        'albums': Album.objects.filter(owner=user),
        'featured_photos': Photo.objects.filter(owner=user, featured=True),
        'newest_photos': Photo.objects.filter(owner=user).order_by('-date_created')[:5],
        'newest_blogs': Blog.objects.filter(owner=user).order_by('-date_created')[:5],
    }


class OwnPortfolioView(AuthenticatedView):
    TEMPLATE = 'portfolio.html'

    def get(self, request):
        return render(request, self.TEMPLATE, get_portfolio_context(request.user))


class PortfolioView(View):
    TEMPLATE = 'portfolio.html'

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise Http404

        return render(request, self.TEMPLATE, get_portfolio_context(user))
