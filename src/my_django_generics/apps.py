from django.apps import AppConfig


class MyDjangoGenericsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.my_django_generics'
