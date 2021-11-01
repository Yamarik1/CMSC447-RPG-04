from django.urls import include, path
from . import views

app_name = 'accounts'

urlpatterns = [
   path('login/', views.login_view, name="login"),
   path('signup/', views.signup_view, name="signup"),
]