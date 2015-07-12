from django.views.generic.base import View
from django.shortcuts import render


class HomeView(View):
    """ Does what it sais... Home sweet Home. """
    TEMPLATE = 'home.html'

    def get(self, request):
        context = {}
        print(request.user.is_anonymous())
        if request.user.is_anonymous():
            context = {
                'no_user': True,
            }
        return render(request, self.TEMPLATE, context)
