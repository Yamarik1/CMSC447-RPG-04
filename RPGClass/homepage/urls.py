from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='Menu'),
    path('mainquest/', views.mainquest, name='mainquest'),
    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
]