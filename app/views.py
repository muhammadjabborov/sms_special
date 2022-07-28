import random

from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, views, permissions
from .service import Util, send_email
# from app.serializers import LoginSerializer


# class LoginApiView(TokenObtainPairView):
#     serializer_class = LoginSerializer
from app.models import User
from app.serializers import RegistrationSerializer, VerifyEmailSerializer, UserDataSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                result = Util.send_email(serializer.validated_data.get('email'))
                return Response(result, status=status.HTTP_201_CREATED)
            except:
                data = {
                    'message': "This username not have in base"
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, 400)


class VertifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                result = send_email(serializer.validated_data.get('activation_code'),
                                    serializer.validated_data.get('email'),
                                    serializer.validated_data.get('username'))
                return Response(result, status=status.HTTP_200_OK)
            except:
                data = {
                    'message_data': 'Error'
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, 404)



class UserList(ListAPIView):
    serializer_class = UserDataSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )


