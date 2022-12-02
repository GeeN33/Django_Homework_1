from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentification import views

urlpatterns = [
    path('create/', views.UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]