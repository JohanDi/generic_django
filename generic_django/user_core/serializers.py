from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]
        extra_field_metadata = {
            'is_staff': {
                'initial': False, # Default value to be pre-filled in the form
            }
        }
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']


class LoginSerializer(Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            return data
        raise ValidationError({'error': 'Invalid email or password.'})

class SudoLoginAsSerializer(serializers.Serializer):
    """Serializer for the view superuser.su_login"""
    id = serializers.IntegerField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_id(self, _id):

        if _id:
            user = self.authenticate(user_id=_id, su=True)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)
        return user

    def validate(self, attrs):
        # We verify that the requesting user is a superuser
        request_user = self.context['request'].user
        if not request_user.is_superuser:
            raise exceptions.ValidationError("Only Superusers can perform a Login-As operation.")
        # We retrieve the user object for which the login is attempt.
        _id = attrs.get('id')
        user = self._validate_id(_id)
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

class SetNewPasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField()
    new_password_1 = serializers.CharField()
    new_password_2 = serializers.CharField()

    def validate_current_password(self, value):
        # Validate that the old_password field is correct.
        request = self.context['request']
        user = request.user
        if not user.check_password(value):
            raise ValidationError(
                'Password not correct',
                code='current_password'
            )
        return value

    def validate(self, data):
        if data['new_password_1'] != data['new_password_2']:
            raise ValidationError('Passwords do not match', code='new_password')
        validate_password(data['new_password_1'])
        return data

class SuLoginSerializer(serializers.Serializer):
    """Serializer for the view superuser.su_login"""
    id = serializers.IntegerField()

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_id(self, _id):

        if _id:
            user = self.authenticate(user_id=_id, su=True)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)
        return user

    def validate(self, attrs):
        # We verify that the requesting user is a supueruser
        request_user = self.context['request'].user
        if not request_user.is_superuser:
            raise exceptions.ValidationError("Only Superusers can perform a Login-As operation.")
        # We retrieve the user object for which the login is attempt.
        _id = attrs.get('id')
        user = self._validate_id(_id)
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs