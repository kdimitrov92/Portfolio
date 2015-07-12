from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from portfolio.logic.accounts import set_default_user_related_data


class RegisterView(View):
    """ View that handles user registration """
    @csrf_exempt
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            set_default_user_related_data(form)

            return redirect("accounts.login")

        return render(request, "register.html", {'form': form, })

    @csrf_exempt
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {'form': form, })
