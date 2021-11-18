from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),
    path('course/', views.course.as_view(), name='course'),
    path('course/<int:pk>/', views.courseSpecific.as_view(), name='courseS'),

    # Url for main quest
    path('course/<int:pk>/mainquest/', views.mainquest.as_view(), name='mainquest'),
    path('course/vTest', views.visualTest, name='test'),
    path('course/<int:course_id>/mainquest/<int:pk>/', views.mainquestView.as_view(), name='mQuestView'),
    path('course/<int:course_id>/mainquest/<int:pk>/quest/', views.mQuestSpecific.as_view(), name="mQuest"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/answer/', views.answer, name="answer"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/summary/', views.summary, name="summary"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/accept/', views.accept, name='accept'),

    # Url for recommendations
    path('course/<int:course_id>/recs/<int:pk>', views.recsView.as_view(), name='recs'),

    # Urls for Bosses
    path('course/<int:pk>/bosses/', views.bosses, name='bosses'),
    path('course/bvTest', views.bossVisualTest, name='bossTest'),
    path('course/<int:course_id>/bosses/<int:pk>/', views.bossView.as_view(), name='bossView'),
    path('course/<int:course_id>/bosses/<int:pk>/boss/', views.bossSpecific.as_view(), name="bosses"),
    path('course/<int:course_id>/bosses/<int:boss_id>/bossAnswer/', views.bossAnswer, name="bossAnswer"),
    path('course/<int:course_id>/bosses/<int:boss_id>/bossSummary/', views.bossSummary, name="bossSummary"),


    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
]