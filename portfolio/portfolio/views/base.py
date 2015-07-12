from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.utils.decorators import method_decorator


class AuthenticatedView(View):
    """ A view that when inherited requires a login for both GET and POST methods of a view class """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AuthenticatedView, self).dispatch(*args, **kwargs)
