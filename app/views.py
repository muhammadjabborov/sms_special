import random

from django.http import Http404
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, views, permissions
from .service import Util, send_email
# from app.serializers import LoginSerializer


# class LoginApiView(TokenObtainPairView):
#     serializer_class = LoginSerializer
from app.models import User, Image
from app.serializers import RegistrationSerializer, VerifyEmailSerializer, UserDataSerializer, LoginSerializer, \
    ImageModelSerializer


class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class RegisterAPIView(GenericAPIView):
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


class VertifyAPIEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                result = send_email(serializer.validated_data.get('activation_code'),
                                    serializer.validated_data.get('email'))
                return Response(result, status=status.HTTP_200_OK)
            except:
                data = {
                    'message_data': 'Error'
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, 404)


class UserAPIList(ListAPIView):
    serializer_class = UserDataSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class ImageModelViewSet(ModelViewSet):
    serializer_class = ImageModelSerializer
    queryset = Image.objects.all()
    lookup_url_kwarg = 'pk'
    parser_classes = (MultiPartParser, )
    permission_classes = (AllowAny,)


    def post(self, request):
        serializer = ImageModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Successfull add your skill'
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        icons = Image.objects.all()
        serializer = ImageModelSerializer(icons, many=True)
        return Response(serializer.data)
