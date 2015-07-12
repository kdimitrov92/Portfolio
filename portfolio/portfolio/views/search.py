from django.shortcuts import render
from django.views.generic.base import View

from portfolio.logic.search import get_search_context


class SearchView(View):
    """ View that handles searches through photos """
    TEMPLATE = 'search.html'

    def get(self, request):
        search_parameters = request.GET.get('search_parameters', '').split(' ')
        return render(request, self.TEMPLATE, get_search_context(search_parameters))
