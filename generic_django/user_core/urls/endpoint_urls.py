from rest_framework.routers import DefaultRouter

from django.urls import path

from ..views import endpoints

app_name = "user_core_api"

router = DefaultRouter()
router.register("user", endpoints.UserViewSet, basename="user")

urlpatterns = router.urls + [
    path('login', endpoints.LoginView.as_view(), name='login'),
    path('logout', endpoints.LogoutView.as_view(), name='logout'),
    path('set_new_password', endpoints.SetNewPasswordView.as_view(), name='set_new_password'),
    path('su_login', endpoints.SudoLoginAsView.as_view(), name='su_login'),
]