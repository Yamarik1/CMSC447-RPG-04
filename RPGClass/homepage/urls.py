from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),
    path('mainquest/', views.mainquest, name='mainquest'),
    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
    path('bosses/', views.bosses, name='bosses'),
]