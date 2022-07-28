from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,TokenObtainPairView
)

# from app.views import LoginApiView
from app.views import RegisterView, VertifyEmailView, UserList

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/',RegisterView.as_view(),name='register'),
    path('user-list/',UserList.as_view(),name='user_list'),
    path('verify-register/',VertifyEmailView.as_view(),name='verify-register')
]
