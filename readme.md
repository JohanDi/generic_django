# my_django_generics
 
Ny Django Generics is a reusable Django app providing enhanced generic views and utilities for rapid development.

The app relies on django_crispy_forms and bootstrap 5 for rapid development of a CRUD interface.

## Features

- Extended generic class-based views for rapid implementation of a CRUD interface.

## Installation

Add `my_django_generics` to your project by adding it to your requirements.txt or installing it directly using pip
   ```bash
   pip install git+<github-url>
   ```

## Configuration

### Required configuration

1. Modify INSTALLED_APPS settings:
   ```
   INSTALLED_APPS = [
       ...
       'crispy_forms',
       'crispy_bootstrap5',
       'my_django_generics',
       ...
   ]
   ```
2. Set crispy forms template pack in your settings.py:
   ```python
   CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
   CRISPY_TEMPLATE_PACK = "bootstrap5"
   ```

### Optional configuration

The following settings are optional but can be configured to customize the behavior of the app:


## Development

This section is about developing of the my_django_generics app.

### Packaging

