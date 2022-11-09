from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('ad/',  views.AdView.as_view()),
    path('ad/<int:pk>/', views.AdDetailView.as_view()),

    path('cat/',  views.CatView.as_view()),
    path('cat/<int:pk>/', views.CatDetailView.as_view())
]
