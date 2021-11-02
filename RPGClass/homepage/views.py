from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render

#prevents people from seeing page until they login in (generic and not assinged to a specific course)
@login_required(login_url="/accounts/login/")
def homepage(request):
    return render(request, 'homepage/menu.html')


def mainquest(request):
    return HttpResponse("Placeholder for the Main Quest page")


def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return HttpResponse("Placeholder for the profile page")