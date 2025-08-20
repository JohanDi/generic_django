from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView

from src.my_django_generics.views import BS5CreateView, BS5UpdateView, BS5DeleteView, BS5ListView

from ..models import User

class CustomLoginView(LoginView):
    template_name = 'my_django_generics/bootstrap5/auth/login.html'
    redirect_authenticated_user = True # Redirects authenticated users to the home page

class CustomLogoutView(LogoutView):
    template_name = 'my_django_generics/bootstrap5/auth/logged_out.html'


class UserListView(LoginRequiredMixin, BS5ListView):
    model = User
    context = {
        'verbose_name': User._meta.verbose_name,
        'verbose_name_plural': User._meta.verbose_name_plural,
        'headers': [
            {'name': 'First Name', 'field': 'first_name'},
            {'name': 'Last Name', 'field': 'last_name'},
            {'name': 'Email', 'field': 'email'},
            {'last_login': 'last_login', 'field': 'last_login', 'format': 'localtime'},
        ],
        # 'create_url': 'user_core:user-create',
        # 'update_url': 'user_core:user-update',
        # 'delete_url': 'user_core:user-delete',
    }

    def get_queryset(self):
        return User.objects.all().order_by('first_name')
