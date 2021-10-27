from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .models import Question, Quest, Choice


def homepage(request):
    return render(request, 'homepage/menu.html')


def mainquest(request):
    return HttpResponse("Placeholder for the Main Quest page")


class mainquestView(generic.DetailView):
    template_name = 'homepage/mQuestView.html'
    model = Quest


class mQuestSpecific(generic.DetailView):
    template_name = "homepage/question.html"
    model = Quest


def answer(request, quest_id, question_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'homepage/question.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    if selected_choice.getCorrect():
        quest.rightAnsChosen()
        quest.save()
        selected_choice.save()

    return HttpResponseRedirect(reverse('homepage:summary', args=(quest.id,)))


def summary(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    return render(request, 'homepage/summary.html', {'quest': quest})


def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return HttpResponse("Placeholder for the profile page")
