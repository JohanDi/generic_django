from django.urls import path

from ..views import pages

app_name = "user_core"

urlpatterns = [
    path("login/", pages.CustomLoginView.as_view(), name="login"),
    path("logout/", pages.CustomLogoutView.as_view(), name="logout"),
    path("users/", pages.UserListView.as_view(), name="user-list"),
]