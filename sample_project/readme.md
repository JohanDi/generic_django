



# App Architecture
- 



# Developer features

## Home page configuration



## Crispy forms

The package `django-crispy-forms` is used to render forms in a more user-friendly way. It allows for
customizing the layout of forms and provides a set of pre-defined templates for rendering forms.

## API Meta endpoints

The metadata of API endpoints where the view class inherits from CustomModelViewSet class (views.py in project base 
folder) can be accessed by adding `/meta` to the endpoint URL. For example, the endpoint `/api/user_core/user/meta/` 
will return the metadata of the `user` endpoint in the `user_core` module. The meta endpoint will return a JSON 
containing information about the fields, their type, whether they are required, read-only and their labels. This is 
useful for generating forms and validating input data.

The meta endpoint can be used by frontend applications to dynamically generate forms based on the
metadata of the API endpoints. This allows for a more flexible and dynamic user interface, as the forms can be
generated based on the available fields in the API endpoints.

The meta endpoint is implemented as an action in the CustomModelViewSet class, defined in the `views.py` file
of the `base` module.

## API Pagination

A custom pagination class was implemented to provide a consistent pagination experience across all API endpoints.
The pagination class can be found in pagination.py of the project's base folder. A paginated response will
include the following fields:
- rows_number: The total number of rows in the response.
- rows_per_page: The number of rows per page.
- page: The current page number.
- results: The list of results for the current page.

## API CustomModelView

## Database configuration

The package dj-database-url allows the developer to configure the database connection using a URL. This
allows for easy configuration of the database connection in different environments, such as development, staging,
and production. The URL can be set in the `DATABASE_URL` environment variable, and the package will automatically
parse the URL and configure the database connection accordingly.

For more information on how to use the package, please refer to the 
[django_database_url documentation](https://pypi.org/project/dj-database-url/)

# Development conventions

## Creating a new app

When creating a new app within the django project, it is recommended to follow the naming conventions:

- Add a python folder 'urls' to the app folder. Create the two files 'endpoint_urls.py' and 'page_urls.py' in the urls 
folder.
- Add a python folder 'views' to the app folder. Create two files 'endpoints.py' and 'pages.py' in the views. 
Alternatively, create two modules 'endpoints' and 'pages' in the views folder containing your own chosen
file structure.
- Add a reference to the project's main urls.py file.



# Log
- Updated Pycharm settings so that the sample p[project finds the django app in the src dir: Django Console:

import sys; print('Python %s on %s' % (sys.version, sys.platform))
import django; print('Django %s' % django.get_version())
from pathlib import Path

BASE_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(BASE_DIR))
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
if 'setup' in dir(django): django.setup()

- Updated Pycharm settings so that the sample project finds the django app in the src dir: Python Console

import sys; print('Python %s on %s' % (sys.version, sys.platform))
from pathlib import Path

BASE_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(BASE_DIR))
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])




