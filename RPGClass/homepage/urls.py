from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),
    path('mainquest/', views.mainquest, name='mainquest'),
    path('mainquest/<int:pk>/', views.mainquestView.as_view(), name='mQuestView'),
    path('mainquest/<int:pk>/quest/', views.mQuestSpecific.as_view(), name="mQuest"),
    path('mainquest/<int:quest_id>/answer/', views.answer, name="answer"),
    path('mainquest/<int:quest_id>/summary/', views.summary, name="summary"),
    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
    path('bosses/', views.bosses, name='bosses'),
]