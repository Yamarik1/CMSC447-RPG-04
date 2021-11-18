from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import Question, Quest, Choice, Boss, bossQuestion, bossChoice, Recs, Topic

# prevents people from seeing page until they login in (generic and not assinged to a specific course)
@login_required(login_url="/accounts/login/")
def homepage(request):
    return render(request, 'homepage/menu.html')


def mainquest(request):
    return render(request, "homepage/mainQuest.html")

def bosses(request):
    return render(request, "homepage/bosses.html")

class mainquestView(generic.DetailView):
    model = Quest
    template_name = 'homepage/mQuestView.html'

class bossView(generic.DetailView):
    model = Boss
    template_name = 'homepage/bossView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context

class recsView(generic.DetailView):
    model = Recs
    template_name = 'homepage/recs.html'

# For the purposes of creating objects in the database easier
def visualTest(request):
    # Delete anything in the database
    for quest in Quest.objects.all():
        quest.delete()

    # Create custom quests with some test values
    # Test Quest 1: using type 1 to give the user questions to answer
    Q = Quest.objects.create(pk=1)
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create(pk=1)
    question.setQuestion("What is 5 + 12?")

    c = question.choice_set.create(pk=1)
    c.setChoice("10")
    c.save()
    c = question.choice_set.create(pk=2)
    c.setChoice("17")
    c.setCorrect(True)
    c.save()

    question.save()
    question = Q.question_set.create(pk=2)
    question.setQuestion("What is 10 - 2?")

    c = question.choice_set.create(pk=3)
    c.setChoice("8")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create(pk=4)
    c.setChoice("12")
    c.save()

    question.save()
    Q.save()

    # Test quest 2: A quest manually updated by the admin (Admin functionality not added yet)
    Q = Quest.objects.create(pk=2)
    Q.setName("Test quest 2")
    Q.setDesc("This quest simulates a quest that would be manually updated by the admin, so it will just direct"
              "straight to the summary page")
    Q.setType(0)
    Q.setXP(10)
    Q.setAvailable(True)
    Q.save()

    return HttpResponseRedirect(reverse('homepage:menu'))

# For the purposes of creating objects in the database easier but used for bosses instead of quests
def bossVisualTest(request):
    # Delete anything in the database
    for boss in Boss.objects.all():
        boss.delete()

    # Create custom boss with some test values
    # Test Boss 1: using type 1 to give the user questions to answer
    Q = Boss.objects.create(pk=1)
    Q.setName("Boss 1")
    Q.setDesc("This is the first test Boss")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    # Creates Questions, choices and answers for the bosses
    bossquestion = Q.bossquestion_set.create(pk=1)
    bossquestion.setQuestion("What is 1 + 1")

    c = bossquestion.bosschoice_set.create(pk=1)
    c.setChoice("2")
    c.setCorrect(True)
    c.save()
    c = bossquestion.bosschoice_set.create(pk=2)
    c.setChoice("13")
    c.save()

    bossquestion.save()
    bossquestion = Q.bossquestion_set.create(pk=2)
    bossquestion.setQuestion("What is 10 - 2?")

    c = bossquestion.bosschoice_set.create(pk=3)
    c.setChoice("8")
    c.setCorrect(True)
    c.save()
    c = bossquestion.bosschoice_set.create(pk=4)
    c.setChoice("12")
    c.save()

    bossquestion.save()

    bossquestion = Q.bossquestion_set.create(pk=3)
    bossquestion.setQuestion("What is the spelling for the word wrong?")

    c = bossquestion.bosschoice_set.create(pk=5)
    c.setChoice("wrong")
    c.setCorrect(True)
    c.save()
    c = bossquestion.bosschoice_set.create(pk=6)
    c.setChoice("right")
    c.save()
    bossquestion.save()

    Q.save()

    return HttpResponseRedirect(reverse('homepage:menu'))

# Adds recommended topics as test
def recsVisualTest(request):
    # Delete anything in the database
    for recs in Recs.objects.all():
        recs.delete()

    # Create custom recommendation with some test values
    # Test recs 1 named recommended topics:
    Q = Recs.objects.create(pk=1)
    Q.setName("Recommended Topics")

    #Creates topics
    topic = Q.topic_set.create(pk=1)
    topic.setTopic("Scoreboards")
    topic.save()

    topic = Q.topic_set.create(pk=2)
    topic.setTopic("Circuts")
    topic.save()

    Q.save()

    return HttpResponseRedirect(reverse('homepage:menu'))

class mQuestSpecific(generic.DetailView):
    queryset = Quest.objects.all()
    template_name = "homepage/question.html"

    def get_context_data(self, **kwargs):
        context = super(mQuestSpecific, self).get_context_data(**kwargs)
        context['question'] = Question.objects.all()
        return context

class bossSpecific(generic.DetailView):
    queryset = Boss.objects.all()
    template_name = "homepage/bossQuestion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context

def answer(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    quest.setXP(0)
    quest.save()
    questionSet = quest.question_set.all()

    # The choice will be check for each question, and the correct counter will increment if the right answer is chosen.
    for question in questionSet:

        selected_choice = question.choice_set.get(pk=request.POST[question.getQuestion()])

        if selected_choice.getCorrect():
            quest.rightAnsChosen()
            quest.save()
            selected_choice.save()

    return HttpResponseRedirect(reverse('homepage:summary', args=(quest.id,)))

def bossAnswer(request, course_id, boss_id):
    boss = get_object_or_404(Boss, pk=boss_id)
    boss.setXP(0)
    boss.save()
    bossSet = boss.bossquestion_set.all()

    # The choice will be check for each question, and the correct counter will increment if the right answer is chosen.
    for bossquestion in bossSet:

        selected_choice = bossquestion.bosschoice_set.get(pk=request.POST[bossquestion.getQuestion()])

        if selected_choice.getCorrect():
            boss.rightAnsChosen()
            boss.save()
            selected_choice.save()

    return HttpResponseRedirect(reverse('homepage:bossSummary', args=(boss.id,)))


def summary(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    return render(request, 'homepage/summary.html', {'quest': quest})

def bossSummary(request, course_id, boss_id):
    boss = get_object_or_404(Boss, pk=boss_id)
    return render(request, 'homepage/bossSummary.html', {'boss': boss})

def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return render(request, 'homepage/bosses.html')

def profile(request):
    return render(request, 'homepage/profile.html')
