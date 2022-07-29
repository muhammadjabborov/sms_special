from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)

# from app.views import LoginApiView
from app.views import RegisterAPIView, VertifyAPIEmailView, UserAPIList, LoginAPIView, ImageModelViewSet

router = DefaultRouter()
router.register('image', ImageModelViewSet, 'image')

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('user-list/', UserAPIList.as_view(), name='user_list'),
    path('verify-register/', VertifyAPIEmailView.as_view(), name='verify-register'),
    path('', include(router.urls)),
]
