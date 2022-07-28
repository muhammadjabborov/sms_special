from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import User


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email', 'activation_code')


# class LoginSerializer(TokenObtainPairSerializer):
#
#     def validate(self, attrs):
#         data = super().validate(attrs)
#
#         refresh = self.get_token(self.user)
#
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         # d = {
#         #     'username ': self.user.username,
#         # }
#         data['data'] = UserDataSerializer(self.user).data
#
#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)
#
#         return data


class RegistrationSerializer(ModelSerializer):

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already taken')
        return email

    class Meta:
        model = User
        fields = ['email']


class VerifyEmailSerializer(ModelSerializer):
    username = CharField(max_length=255)
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email hasn't in base")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already taken')
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'activation_code']

