from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render



def homepage(request):
    return render(request, 'homepage/menu.html')


def mainquest(request):
    return HttpResponse("Placeholder for the Main Quest page")


def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return render(request, 'homepage/profile.html')
