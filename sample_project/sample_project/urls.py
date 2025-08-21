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
from rest_framework.reverse import reverse_lazy


class CustomApiRootView(TemplateView):
    """This view serves as the root for the API, providing a simple response indicating that the API is available."""

    template_name = 'my_django_generics.root_api.html'

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
    path('user_core/', include('sample_project.user_core.urls.endpoint_urls')),
]

django_page_urlpatterns = [
    path('user_core/', include('sample_project.user_core.urls.page_urls')),
    path('inventory_app/', include('sample_project.inventory_app.urls.page_urls')),
]

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('inventory_app:section-list'))),
    path('admin/', admin.site.urls),
    path('pages/', include(django_page_urlpatterns)),
    path('api/', include(api_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
