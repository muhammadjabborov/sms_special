from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.settings import api_settings

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import User, Image


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'activation_code')


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['data'] = UserDataSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegistrationSerializer(Serializer):
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    email = CharField(max_length=255)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already taken')
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already taken')
        return username

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class VerifyEmailSerializer(ModelSerializer):

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise ValidationError("This email hasn't in base")
        return email

    class Meta:
        model = User
        fields = ['email', 'activation_code']


class ImageModelSerializer(ModelSerializer):
    title = CharField(max_length=255)

    def validate_title(self, title):
        if Image.objects.filter(title=title).exists():
            raise ValidationError('This name skill already taken')
        return title

    class Meta:
        model = Image
        exclude = ()
