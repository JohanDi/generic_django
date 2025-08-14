from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models import Section, Compartment

class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'generic_table_page.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name')
        valid_fields = ['name', 'description']
        field = order_by.lstrip('-')
        if field in valid_fields:
            queryset = queryset.order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = Section._meta.verbose_name
        context['verbose_name_plural'] = Section._meta.verbose_name_plural
        context['headers'] = [
            {'name': 'Name', 'field': 'name'},
            {'name': 'Description', 'field': 'description'},
        ]
        context['create_url'] = 'inventory_app:section-create'
        context['update_url'] = 'inventory_app:section-update'
        context['delete_url'] = 'inventory_app:section-delete'
        return context

class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    template_name = 'generic_form_page.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:section-list')

    def get_success_url(self):
        messages.success(self.request, 'Section created successfully.')
        return super().get_success_url()

class SectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Section
    template_name = 'generic_form_page.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:section-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, 'Section updated successfully.')
        return super().get_success_url()

class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section
    # template_name = 'inventory_app/section_confirm_delete.html'
    success_url = reverse_lazy('inventory_app:section-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_delete'] = True
        return context

    # Add a success message or confirmation if needed
    def get_success_url(self):

        messages.success(self.request, 'Section deleted successfully.')
        return super().get_success_url()

class CompartmentListView(LoginRequiredMixin, ListView):
    model = Compartment
    template_name = 'generic_table_page.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name')
        valid_fields = ['name', 'description']
        field = order_by.lstrip('-')
        if field in valid_fields:
            queryset = queryset.order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = Compartment._meta.verbose_name
        context['verbose_name_plural'] = Compartment._meta.verbose_name_plural
        context['headers'] = [
            {'name': 'Name', 'field': 'name'},
            {'name': 'Description', 'field': 'description'},
            {'name': 'Section', 'field': 'section.name'},
        ]
        context['create_url'] = 'inventory_app:compartment-create'
        context['update_url'] = 'inventory_app:compartment-update'
        context['delete_url'] = 'inventory_app:compartment-delete'
        return context

class CompartmentCreateView(LoginRequiredMixin, CreateView):
    model = Compartment
    template_name = 'generic_form_page.html'
    fields = ['name', 'description', 'section']
    success_url = reverse_lazy('inventory_app:compartment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        context['verbose_name'] = 'compartment'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Compartment created successfully.')
        return super().get_success_url()

class CompartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Compartment
    template_name = 'generic_form_page.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('inventory_app:compartment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['verbose_name'] = 'compartment'
        return context

class CompartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Compartment
    # template_name = 'inventory_app/section_confirm_delete.html'
    success_url = reverse_lazy('inventory_app:compartment-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_delete'] = True
        return context

    # Add a success message or confirmation if needed
    def get_success_url(self):
        messages.success(self.request, 'Compartment deleted successfully.')
        return super().get_success_url()