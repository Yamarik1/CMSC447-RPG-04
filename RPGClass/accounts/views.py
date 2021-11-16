from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UpdateForm, SignUpForm


# Create your views here.
def signup_view(request):
    #when the user enters data for the signup sheet
    if request.method == 'POST':
        #checks validations such as if we already have a user in the database or if what they enter is valid
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() #load profile instance
            user.student.setStudentName(user.username)
            user.student.setNickname(user.username)
            user.save()
            #log user in
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            #after successfully created an account, send them to the homepage
            return redirect('homepage:menu')
    #sends back a blank form of the sign up sheet to sign up
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request, user)
            return redirect('homepage:menu')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')


def update_profile(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('user_name')
            if form.validate(username=username, password=password):
                user.student.setNickname(form.cleaned_data['nickname'])
                user.save()
                return redirect('homepage:profile')
        else:
            return redirect('homepage:menu')
    else:
        form = UpdateForm()
    return render(request, 'accounts/profile_update.html',{'form': form} )
