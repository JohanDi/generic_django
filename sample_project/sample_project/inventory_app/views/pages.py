from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from ..models import Section, Compartment

from src.my_django_generics.views import BS5ListView, BS5CreateView, BS5UpdateView, BS5DeleteView

class SectionListView(LoginRequiredMixin, BS5ListView):
    model = Section
    paginate_by = 10

    context = {
        'verbose_name': Section._meta.verbose_name,
        'verbose_name_plural': Section._meta.verbose_name_plural,
        'headers': [
            {'name': 'Name', 'field': 'name'},
            {'name': 'Description', 'field': 'description'},
        ],
        'create_url': 'inventory_app:section-create',
        'update_url': 'inventory_app:section-update',
        'delete_url': 'inventory_app:section-delete',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name')
        valid_fields = ['name', 'description']
        field = order_by.lstrip('-')
        if field in valid_fields:
            queryset = queryset.order_by(order_by)
        return queryset

class SectionCreateView(LoginRequiredMixin, BS5CreateView):
    model = Section
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:section-list')

class SectionUpdateView(LoginRequiredMixin, BS5UpdateView):
    model = Section
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:section-list')

class SectionDeleteView(LoginRequiredMixin, BS5DeleteView):
    model = Section
    success_url = reverse_lazy('inventory_app:section-list')

class CompartmentListView(LoginRequiredMixin, BS5ListView):
    model = Compartment
    paginate_by = 10

    context = {
        'verbose_name': Compartment._meta.verbose_name,
        'verbose_name_plural': Compartment._meta.verbose_name_plural,
        'headers': [
            {'name': 'Name', 'field': 'name'},
            {'name': 'Description', 'field': 'description'},
            {'name': 'Section', 'field': 'section.name'},
        ],
        'create_url': 'inventory_app:compartment-create',
        'update_url': 'inventory_app:compartment-update',
        'delete_url': 'inventory_app:compartment-delete',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name')
        valid_fields = ['name', 'description']
        field = order_by.lstrip('-')
        if field in valid_fields:
            queryset = queryset.order_by(order_by)
        return queryset


class CompartmentCreateView(LoginRequiredMixin, BS5CreateView):
    model = Compartment
    fields = ['name', 'description', 'section']
    success_url = reverse_lazy('inventory_app:compartment-list')

class CompartmentUpdateView(LoginRequiredMixin, BS5UpdateView):
    model = Compartment
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:compartment-list')

class CompartmentDeleteView(LoginRequiredMixin, BS5DeleteView):
    model = Compartment
    success_url = reverse_lazy('inventory_app:compartment-list')

    # Add a success message or confirmation if needed
    def get_success_url(self):
        messages.success(self.request, 'Compartment deleted successfully.')
        return super().get_success_url()