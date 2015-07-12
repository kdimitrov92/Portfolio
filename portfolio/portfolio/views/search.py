from django.shortcuts import render, redirect
from django.views.generic.base import View

from portfolio.logic.search import get_search_context


class SearchView(View):
    """ View that handles searches through photos """
    TEMPLATE = 'search.html'

    def get(self, request):
        search_parameters = request.GET.get('search_parameters', '').split(' ')
        if not search_parameters:
            return redirect('portfolio.home')

        print(search_parameters)
        return render(request, self.TEMPLATE, get_search_context(search_parameters))
