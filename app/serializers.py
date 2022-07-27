from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import User


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


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

    class Meta:
        model = User
        fields = ['activation_code','email']



