from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentification import views

urlpatterns = [
     # path('create/', views.UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    path('', views.UsersListView.as_view()),
    path('<int:pk>/', views.UsersDetailView.as_view()),
    path('create/', views.UsersCreateView.as_view()),
    path('<int:pk>/update/', views.UsersUpdateView.as_view()),
    path('<int:pk>/delete/', views.UsersDeleteView.as_view()),
    path('Z/', views.UsersZView.as_view()),
]