from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView

from generic_django.user_core.models import User


def index(request):
    return render(request, 'user_core/index.html')

class CustomLoginView(LoginView):
    template_name = 'user_core/login.html'
    redirect_authenticated_user = True # Redirects authenticated users to the home page

class CustomLogoutView(LogoutView):
    # next_page = 'home'
    template_name = 'user_core/logged_out.html'


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_core/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all().order_by('first_name')
