from django.urls import path

from ..views import pages

app_name = "inventory_app"

urlpatterns = [
    path("section/list/", pages.SectionListView.as_view(), name="section-list"),
    path("section/create/", pages.SectionCreateView.as_view(), name="section-create"),
    path("section/update/<int:pk>/", pages.SectionUpdateView.as_view(), name="section-update"),
    path("section/delete//<int:pk>/", pages.SectionDeleteView.as_view(), name="section-delete"),
    path("compartment/list/", pages.CompartmentListView.as_view(), name="compartment-list"),
    path("compartment/create/", pages.CompartmentCreateView.as_view(), name="compartment-create"),
    path("compartment/update/<int:pk>/", pages.CompartmentUpdateView.as_view(), name="compartment-update"),
    path("compartment/delete/<int:pk>/", pages.CompartmentDeleteView.as_view(), name="compartment-delete"),
]