from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.models import Session
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from ...views import CustomModelViewSet

from ..models import User
from ..serializers import LoginSerializer, UserSerializer, SudoLoginAsSerializer, SetNewPasswordSerializer, SuLoginSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)
UserModel = get_user_model()

class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['first_name', 'last_name', 'email']
    # search_fields: fields to search in for values provided in the search query parameter


class LoginView(GenericAPIView):

    response_serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def __init__(self):
        super(LoginView, self).__init__()
        self.serializer = None
        self.user = None
        return

    @sensitive_post_parameters_m
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def login(self):
        """Custom logic: Disable the creation of a token."""

        credentials = self.serializer.validated_data
        self.user = authenticate(self.request, **credentials)
        django_login(self.request, self.user)

    def get_response(self):
        """Custom logic: Disable working with token"""
        serializer = self.response_serializer_class(instance=self.user, context={'request': self.request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        """Custom logic: Do not raise an exception when serializer is invalid. Instead, put the error in the http response
        """

        self.serializer = self.get_serializer(data=request.data, context={'request': request})
        if self.serializer.is_valid(raise_exception=False):
            self.login()
            return self.get_response()
        else:
            return Response({'errors': self.serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LogoutView(GenericAPIView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        django_logout(request)
        return HttpResponse()


class AuthCheck(APIView):
    permission_classes = []

    def get(self, request):
        if request.user.is_authenticated:
            user = UserSerializer(request.user, context={'request': request})
            return Response({"isAuthenticated": True, "user": user.data})
        else:
            return Response({"isAuthenticated": False})


def expire_session_view(request, session_key):
    """
    This view allows a user to expire a session by its session key.
    :param request:
    :param session_key:
    :return:
    """
    try:
        session = Session.objects.get(session_key=session_key)
        session.delete()
    except Session.DoesNotExist:
        pass
    return HttpResponseRedirect('/admin/sessions/session/')


class SetNewPasswordView(GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        """Custom logic: Do not raise an exception when serializer is invalid. Instead, put the error in the http response
        """
        self.serializer = self.get_serializer(data=request.data)
        if self.serializer.is_valid(raise_exception=False):
            user = request.user
            new_password = self.serializer.validated_data['new_password_1']
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'errors': self.serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SudoLoginAsView(GenericAPIView):
    """This view allows a superuser to login as another user."""

    response_serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    serializer_class = SudoLoginAsSerializer

    def __init__(self):
        super(SudoLoginAsView, self).__init__()
        self.serializer = None
        self.user = None
        return

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(SudoLoginAsView, self).dispatch(request, *args, **kwargs)

    def login(self):

        self.user = self.serializer.validated_data['user']
        if not self.user:
            raise Http404("User not found")

        exit_users_pk = self.request.session.get("exit_users_pk", default=[])
        exit_users_pk.append(
            (self.request.session[SESSION_KEY], self.request.session[BACKEND_SESSION_KEY]))

        # Ensure last_login timestamp is not altered by the admin login
        last_login = self.user.last_login
        try:
            django_login(self.request, self.user)
            self.request.session["exit_users_pk"] = exit_users_pk
        finally:
            self.user.last_login = last_login
            self.user.save(update_fields=['last_login'])

    def get_response(self):
        """Fetch the user with the response serializer"""
        serializer = self.response_serializer_class(instance=self.user, context={'request': self.request})
        response = Response({**serializer.data, 'impostor': True}, status=status.HTTP_200_OK)
        return response

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        """
        Custom logic: Do not raise an exception when serializer is valid. Instead, put the error in the http response.
        """
        self.serializer = self.get_serializer(data=request.data, context={'request': request})
        if self.serializer.is_valid(raise_exception=False):
            self.login()
            return self.get_response()
        else:
            return Response({'errors': self.serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

