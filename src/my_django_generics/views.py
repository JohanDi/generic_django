from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

class BS5ListView(ListView):
    """
    A generic ListView that uses Bootstrap 5 for rendering.
    This class can be extended to create custom list views with Bootstrap 5 styling.
    """
    template_name = 'my_django_generics/bootstrap5/generic_table_page.html'

    context = {
        'verbose_name': None,
        'verbose_name_plural': None,
        'headers': None, # list of dictionaries with 'name' and 'field' keys, and optional 'format' key
        'create_url': None,
        'update_url': None,
        'delete_url': None,
    }

    def verify_context(self):
        """
        Verify that the context has all required keys.
        If any key is missing, raise an error.
        """

        required_keys = ['verbose_name', 'verbose_name_plural', 'headers']
        for key in required_keys:
            if self.context[key] is None:
                raise ValueError(f'Missing required context key: {key}. '
                                 f'Define it in the context dictionary attribute of the view class.')


    def get_context_data(self, **kwargs):
        self.verify_context()
        context = super().get_context_data(**kwargs)
        context.update(self.context)
        return context

class BS5CreateView(CreateView):
    """
    A generic CreateView that uses Bootstrap 5 for rendering.
    This class can be extended to create custom forms with Bootstrap 5 styling.
    """
    template_name = 'my_django_generics/bootstrap5/generic_form_page.html'


    def get_success_url(self):
        # Get verbose name of model
        verbose_name = self.model._meta.verbose_name
        messages.success(self.request, f'{verbose_name.capitalize()} created successfully.')
        return super().get_success_url()

class BS5UpdateView(UpdateView):
    """
    A generic UpdateView that uses Bootstrap 5 for rendering.
    This class can be extended to create custom update forms with Bootstrap 5 styling.
    """
    template_name = 'my_django_generics/bootstrap5/generic_form_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

    def get_success_url(self):
        # Get verbose name of model
        verbose_name = self.model._meta.verbose_name
        messages.success(self.request, f'{verbose_name.capitalize()} updated successfully.')
        return super().get_success_url()

class BS5DeleteView(DeleteView):
    """
    A generic DeleteView that uses Bootstrap 5 for rendering.
    This class can be extended to create custom delete confirmation pages with Bootstrap 5 styling.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_delete'] = True
        return context

    def get_success_url(self):
        # Get verbose name of model
        verbose_name = self.model._meta.verbose_name
        messages.success(self.request, f'{verbose_name.capitalize()} deleted successfully.')
        return super().get_success_url()