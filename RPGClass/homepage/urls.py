from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),
    path('course/', views.course.as_view(), name='course'),
    path('course/<int:pk>/', views.courseSpecific.as_view(), name='courseS'),


    # Url for main quest

    path('course/<int:pk>/mainquest/', views.mainquest.as_view(), name='mainquest'),
    path('course/<int:course_id>/marketplace/', views.marketplace, name="marketplace"),
    path('course/<int:course_id>/course_profile/', views.course_profile, name="course_profile"),
    path('course/vTest', views.visualTest, name='test'),
    path('course/aTest', views.accountTest, name='aTest'),
    path('course/cTest', views.courseIni, name='cTest'),
    path('course/<int:course_id>/mainquest/<int:pk>/', views.mainquestView.as_view(), name='mQuestView'),
    path('course/<int:course_id>/mainquest/<int:pk>/quest/', views.mQuestSpecific.as_view(), name="mQuest"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/answer/', views.answer, name="answer"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/summary/', views.summary, name="summary"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/accept/', views.accept, name='accept'),
    path('course/<int:course_id>/initialize', views.skillscreate, name='skill_in'),
    path('course/<int:course_id>/Cstudent', views.create_course_student, name='course_student'),
    path('sidequest/', views.sidequest, name='sidequest'),

    # Url for recommendations
    path('course/<int:course_id>/recs/<int:pk>', views.recsView.as_view(), name='recs'),

    # Url for topics to improve on
    path('course/<int:course_id>/improve/<int:pk>', views.improveView.as_view(), name='improve'),

    # Urls for Bosses
    path('course/<int:pk>/bosses/', views.bosses.as_view(), name='bosses'),
    path('course/<int:course_id>/bosses/<int:pk>/', views.bossView.as_view(), name='bossView'),
    path('course/<int:course_id>/bosses/<int:pk>/boss/', views.bossSpecific.as_view(), name="bosses"),
    path('course/<int:course_id>/bosses/<int:boss_id>/bossAnswer/', views.bossAnswer, name="bossAnswer"),
    path('course/<int:course_id>/bosses/<int:boss_id>/bossSummary/', views.bossSummary, name="bossSummary"),
    path('course/<int:course_id>/bosses/<int:boss_id>/accept/', views.bAccept, name='bAccept'),
   
   
    path('course/<int:pk>/sidequest/', views.sidequest.as_view(), name='sidequest'),
    path('course/<int:course_id>/sidequest/<int:pk>/', views.sidequestView.as_view(), name='sQuestView'),
    path('course/<int:course_id>/sidequest/<int:pk>/squest/', views.sQuestSpecific.as_view(), name="sQuest"),
    path('course/<int:course_id>/sidequest/<int:sidequest_id>/answer/', views.sAnswer, name="sAnswer"),
    path('course/<int:course_id>/sidequest/<int:sidequest_id>/summary/', views.sQuestSummary, name="sQuestSummary"),
    path('course/<int:course_id>/sidequest/<int:sidequest_id>/accept/', views.sAccept, name='sAccept'),

    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>', views.profileSpecific.as_view(), name='profileS'),

    path('course/<int:course_id>/leaderboard', views.leaderboard.as_view(), name='leaderboard'),
    

]