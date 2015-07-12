from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View

from portfolio.views.base import AuthenticatedView
from portfolio.logic.portfolios import get_portfolio_context


class OwnPortfolioView(AuthenticatedView):
    """
    A view for a users personal portfolio that can only be accessed if authenticated

    NOTE: This will be updated to an edit portfolio view where only the person accessing it sees
    an edit form for his own portfolio
    """
    TEMPLATE = 'portfolio_view.html'

    def get(self, request):
        return render(request, self.TEMPLATE, get_portfolio_context(request.user))


class PortfolioView(View):
    """ A view for any persons portfolio that is publically accessable """
    TEMPLATE = 'portfolio_view.html'

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise Http404

        return render(request, self.TEMPLATE, get_portfolio_context(user))
