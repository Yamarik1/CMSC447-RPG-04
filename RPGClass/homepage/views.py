from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .models import Question, Quest, Choice


def homepage(request):
    return render(request, 'homepage/menu.html')


def mainquest(request):
    return render(request, "homepage/mainQuest.html")

class mainquestView(generic.DetailView):
    template_name = 'homepage/mQuestView.html'
    model = Quest


class mQuestSpecific(generic.DetailView):
    queryset = Quest.objects.all()
    template_name = "homepage/question.html"

    def get_context_data(self, **kwargs):
        context = super(mQuestSpecific, self).get_context_data(**kwargs)
        context['question'] = Question.objects.all()
        return context


def answer(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    quest.setRight(0)
    quest.save()
    questionSet = quest.question_set.all()

    for question in questionSet:

        selected_choice = question.choice_set.get(pk=request.POST[question.getQuestion()])

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
