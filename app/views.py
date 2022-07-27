import random

from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, views, permissions
from .utils import Util
# from app.serializers import LoginSerializer


# class LoginApiView(TokenObtainPairView):
#     serializer_class = LoginSerializer
from app.models import User
from app.serializers import RegistrationSerializer, VerifyEmailSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.validated_data
        message_data = {'message': 'Pleas check your email'}
        user = User.objects.get(email=user_data['email'])
        email_subject = 'Hi ' + user.email + ' Please take your activation code'
        email_body = str(random.randint(1000, 10000))
        user.activation_code = email_body
        user.save()
        data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'to_email': user.email
        }
        Util.send_email(data)
        return Response(message_data, status=status.HTTP_201_CREATED)


class VertifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data.get('email'))

        message_data = {
            'message': 'Successfull'
        }
        error_message_data = {
            'message': 'Bad Request'
        }
        if user.activation_code == serializer.validated_data.get("activation_code"):
            user.is_verified = True
            user.save()
            return Response(message_data, status=status.HTTP_200_OK)
        return Response(error_message_data, status=status.HTTP_400_BAD_REQUEST)
