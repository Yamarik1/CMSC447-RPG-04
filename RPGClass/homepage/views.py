from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


from .models import Course, Question, Quest, Choice, Boss, bossQuestion, bossChoice, Recs, Topic


# prevents people from seeing page until they login in (generic and not assinged to a specific course)
@login_required(login_url="/accounts/login/")
def homepage(request):
    return render(request, 'homepage/menu.html')


class course(generic.ListView):
    template_name = 'homepage/course.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()


class courseSpecific(generic.DetailView):
    model = Course
    template_name = 'homepage/courseS.html'


class mainquest(generic.DetailView):
    model = Course
    template_name = 'homepage/mainQuest.html'

class bosses(generic.DetailView):
    model = Course
    template_name = 'homepage/bosses.html'

class mainquestView(generic.DetailView):
    model = Quest
    template_name = 'homepage/mQuestView.html'

class bossView(generic.DetailView):
    model = Boss
    template_name = 'homepage/bossView.html'

    # Pass the course_id in the url to the html file so that the urls can stay consistent
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class mQuestSpecific(generic.DetailView):
    queryset = Quest.objects.all()
    template_name = "homepage/question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


def answer(request, course_id, quest_id):
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
    # When the quest is finished, the number of lives is decreased by one
    quest.subHeart()
    quest.save()

    return HttpResponseRedirect(reverse('homepage:summary', args=(course_id, quest.id,)))


def summary(request, course_id, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'homepage/summary.html', {'quest': quest, 'course': course})


# Function added to allow the user to accept the result of the quest
def accept(request, course_id, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = quest.getXP()
    # XP for the course will get updated after the accept button is chosen.
    course.updateXP(gainedXP)

    course.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))


# Implementation of side quests is the same of main quests, just with a different table in the database
class sidequest(generic.DetailView):
    model = Course
    template_name = 'homepage/sideQuest.html'


class sidequestView(generic.DetailView):
    model = SideQuest
    template_name = 'homepage/sQuestView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class sQuestSpecific(generic.DetailView):
    queryset = SideQuest.objects.all()
    template_name = "homepage/sQuestQuestion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


class recsView(generic.DetailView):
    model = Recs
    template_name = 'homepage/recs.html'


def sAnswer(request, course_id, sidequest_id):
    sidequest = get_object_or_404(SideQuest, pk=sidequest_id)
    sidequest.setXP(0)
    sidequest.save()
    questionSet = sidequest.question_set.all()

    # The choice will be check for each question, and the correct counter will increment if the right answer is chosen.
    for question in questionSet:

        selected_choice = question.choice_set.get(pk=request.POST[question.getQuestion()])

        if selected_choice.getCorrect():
            sidequest.rightAnsChosen()
            sidequest.save()
            selected_choice.save()

    sidequest.subHeart()
    sidequest.save()

    return HttpResponseRedirect(reverse('homepage:sQuestSummary', args=(course_id, sidequest.id,)))


def sQuestSummary(request, course_id, sidequest_id):
    sidequest = get_object_or_404(SideQuest, pk=sidequest_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'homepage/sQuestSummary.html', {'sidequest': sidequest, 'course': course})


def sAccept(request, course_id, sidequest_id):
    sidequest = get_object_or_404(SideQuest, pk=sidequest_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = sidequest.getXP()

    course.updateXP(gainedXP)

    course.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return render(request, 'homepage/profile.html')


# For the purposes of creating objects in the database easier
def visualTest(request):
    # Delete anything in the database

    for newCourse in Course.objects.all():
        newCourse.delete()

    newCourse = Course.objects.create(pk=1)
    newCourse.setName("Fus Ro Dah")
    newCourse.setSection(1)
    newCourse.setMaxXP(5)

    # Create custom quests with some test values
    # Test Quest 1: using type 1 to give the user questions to answer
    Q = newCourse.quest_set.create(pk=1)
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create(pk=1)
    question.setQuestion("What is the answer to life, the universe, and everything")

    c = question.choice_set.create(pk=1)
    c.setChoice("Food")
    c.save()
    c = question.choice_set.create(pk=2)
    c.setChoice("42")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create(pk=3)
    c.setChoice("...what?")
    c.save()

    question.save()
    question = Q.question_set.create(pk=2)
    question.setQuestion("Pineapple on Pizza?")

    c = question.choice_set.create(pk=4)
    c.setChoice("No")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create(pk=5)
    c.setChoice("Yes")
    c.save()

    question.save()
    Q.save()

    newCourse.save()
    # Test quest 2: A quest manually updated by the admin (Admin functionality not added yet)
    Q = newCourse.quest_set.create(pk=2)
    Q.setName("Test quest 2")
    Q.setDesc("This quest simulates a quest that would be manually updated by the admin, so it will just direct"
              "straight to the summary page")
    Q.setType(0)
    Q.setXP(7)
    Q.setAvailable(True)
    Q.save()
    
    newCourse.save()

    squest = newCourse.sidequest_set.create(pk=1)
    squest.setName("Side Quest 1")
    squest.setType(1)
    squest.setLives(5)
    squest.setAvailable(True)

    question = squest.question_set.create(pk=3)
    question.setQuestion("test")
    question.save()
    c = question.choice_set.create(pk=6)
    c.setChoice("Right")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create(pk=7)
    c.setChoice("Wrong")
    c.save()
    squest.save()
    newCourse.save()

    C = Course.objects.create(pk=2)
    C.setName("Course 2")
    C.setMaxXP(10)
    
    Q = C.quest_set.create(pk=3)
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)
    
    question = Q.question_set.create(pk=4)
    question.setQuestion("What is 10 + 1?")
    
    c = question.choice_set.create(pk=8)
    c.setChoice("10")
    c.save()
    c = question.choice_set.create(pk=9)
    c.setChoice("11")
    c.setCorrect(True)
    c.save()
    
    question.save()
    question = Q.question_set.create(pk=5)
    question.setQuestion("What is 8 - 2?")

    c = question.choice_set.create(pk=10)
    c.setChoice("6")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create(pk=11)
    c.setChoice("12")
    c.save()
    question.save()
    Q.save()

    C.save()
    
    
    # Set up the bosses database table

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
    
    #Set up the recommended topics visual test
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
    
class bossSpecific(generic.DetailView):
    queryset = Boss.objects.all()
    template_name = "homepage/bossQuestion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context



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


def bossSummary(request, course_id, boss_id):
    boss = get_object_or_404(Boss, pk=boss_id)
    return render(request, 'homepage/bossSummary.html', {'boss': boss})






   
