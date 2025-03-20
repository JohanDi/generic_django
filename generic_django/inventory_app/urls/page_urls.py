from django.urls import path

from ..views import pages

app_name = "inventory_app"

urlpatterns = [
    path("section/list/", pages.SectionListView.as_view(), name="section-list"),
    path("section/create/", pages.SectionCreateView.as_view(), name="section-create"),
    path("section/update/<int:pk>/", pages.SectionUpdateView.as_view(), name="section-update"),
    path("section/delete//<int:pk>/", pages.SectionDeleteView.as_view(), name="section-delete"),
]