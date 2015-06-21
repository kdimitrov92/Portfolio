from django.views.generic.base import View
from django.shortcuts import render


class PortfolioView(View):
    TEMPLATE = 'home.html'

    def get(self, request):
        context = {}
        return render(request, self.TEMPLATE, context)
