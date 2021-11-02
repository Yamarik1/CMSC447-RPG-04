from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


# Create your views here.
def signup_view(request):
    #when the user enters data for the signup sheet
    if request.method == 'POST':
        #checks validations such as if we already have a user in the database or if what they enter is valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log user in
            login(request, user)
            #after successfully created an account, send them to the homepage
            return redirect('homepage:menu')
    #sends back a blank form of the sign up sheet to sign up
    else:
        form = UserCreationForm()
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
