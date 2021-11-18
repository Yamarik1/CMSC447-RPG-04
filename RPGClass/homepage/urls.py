from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path('', views.homepage, name='menu'),
    path('course/', views.course.as_view(), name='course'),
    path('course/<int:pk>/', views.courseSpecific.as_view(), name='courseS'),
    path('course/<int:pk>/mainquest/', views.mainquest.as_view(), name='mainquest'),
    path('course/<int:pk>/marketplace/', views.marketplace.as_view(), name="marketplace"),
    path('course/vTest', views.visualTest, name='test'),
    path('course/<int:course_id>/mainquest/<int:pk>/', views.mainquestView.as_view(), name='mQuestView'),
    path('course/<int:course_id>/mainquest/<int:pk>/quest/', views.mQuestSpecific.as_view(), name="mQuest"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/answer/', views.answer, name="answer"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/summary/', views.summary, name="summary"),
    path('course/<int:course_id>/mainquest/<int:quest_id>/accept/', views.accept, name='accept'),
    path('course/<int:course_id>/initialize', views.skillscreate, name='skill_in'),
    path('course/<int:course_id>/Cstudent', views.create_course_student, name='course_student'),
    path('sidequest/', views.sidequest, name='sidequest'),
    path('profile/', views.profile, name='profile'),
    path('bosses/', views.bosses, name='bosses'),
]