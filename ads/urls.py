from django.urls import path
from ads import views

urlpatterns = [
    path('', views.index),
    path('users/', views.UsersListView.as_view()),
    path('users/<int:pk>/', views.UsersDetailView.as_view()),
    path('users/create/', views.UsersCreateView.as_view()),
    path('users/<int:pk>/update/', views.UsersUpdateView.as_view()),
    path('users/<int:pk>/delete/', views.UsersDeleteView.as_view()),
    path('users/Z/', views.UsersZView.as_view()),


    path('ad/', views.AdListView.as_view()),
    path('ad/<int:pk>/update/', views.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view()),
    path('ad/<int:pk>/', views.AdDetailView.as_view()),
    path('ad/create/', views.AdCreateView.as_view()),
    path('ad/<int:pk>/upload_image/', views.AdImageView.as_view()),

    path('selection/create/', views.SelectionCreateView.as_view()),
    path('selection/', views.SelectionListView.as_view()),
    path('selection/<int:pk>/', views.SelectionDetailView.as_view()),
    path('selection/<int:pk>/update/', views.SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', views.SelectionDeleteView.as_view()),

]