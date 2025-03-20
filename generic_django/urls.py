"""
URL configuration for USAHE_Partfinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path, include
from django.views.generic import RedirectView, View, TemplateView
from django.conf import settings
from django.shortcuts import resolve_url


class CustomApiRootView(TemplateView):
    """This view serves as the root for the API, providing a simple response indicating that the API is available."""

    template_name = 'rest_framework/root.html'

    def get_context_data(self, **kwargs):
        """Return the context data for the API root view."""
        context = super().get_context_data(**kwargs)
        context['breadcrumblist'] = [('/api/', '/api/')]
        context['app_api_root_points'] = [
            ('User Core', 'user_core_api:api-root'),
        ]
        return context


api_urlpatterns = [
    path('', CustomApiRootView.as_view(), name='api-root'),
    path('user_core/', include('generic_django.user_core.urls.endpoint_urls')),
]

django_page_urlpatterns = [
    path('user_core/', include('generic_django.user_core.urls.page_urls')),
    path('inventory_app/', include('generic_django.inventory_app.urls.page_urls')),
]


class HomeView(LoginRequiredMixin, View):
    """This view checks if the setting HOME_REDIRECT_URL is set and redirects to that URL if it is.
    If it is not set, it renders the home.html template.
    """
    def get(self, request, *args, **kwargs):
        # print(request.META.get('HTTP_REFERER'))
        if hasattr(settings, 'HOME_REDIRECT_URL') and settings.HOME_REDIRECT_URL:
            return RedirectView.as_view(url=resolve_url(settings.HOME_REDIRECT_URL))(request)
        else:
            return TemplateResponse(request, 'home.html', {
                'breadcrumblist': [('/', '/')],
                'title': 'Home',
            })

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('pages/', include(django_page_urlpatterns)),
    path('api/', include(api_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
