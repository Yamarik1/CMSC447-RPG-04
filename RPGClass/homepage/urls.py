from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),

    # Urls for Quests
    path('mainquest/', views.mainquest, name='mainquest'),
    path('mainquest/vTest', views.visualTest, name='test'),
    path('mainquest/rvTest', views.recsVisualTest, name='recsTest'),
    path('mainquest/<int:pk>/', views.mainquestView.as_view(), name='mQuestView'),
    path('mainquest/<int:pk>/quest/', views.mQuestSpecific.as_view(), name="mQuest"),
    path('mainquest/<int:quest_id>/answer/', views.answer, name="answer"),
    path('mainquest/<int:quest_id>/summary/', views.summary, name="summary"),

    # Url for recommendations
    path('recs/<int:pk>', views.recsView.as_view(), name='recs'),

    # Urls for Bosses
    path('bosses/', views.bosses, name='bosses'),
    path('bosses/bvTest', views.bossVisualTest, name='bossTest'),
    path('bosses/<int:pk>/', views.bossView.as_view(), name='bossView'),
    path('bosses/<int:pk>/boss/', views.bossSpecific.as_view(), name="bosses"),
    path('bosses/<int:boss_id>/bossAnswer/', views.bossAnswer, name="bossAnswer"),
    path('bosses/<int:boss_id>/bossSummary/', views.bossSummary, name="bossSummary"),


    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
]