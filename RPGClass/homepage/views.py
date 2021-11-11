from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import Course, Question, Quest, Choice


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


# def mainquest(request, course_id):
# return render(request, "homepage/mainQuest.html")


class mainquestView(generic.DetailView):
    model = Quest
    template_name = 'homepage/mQuestView.html'


# For the purposes of creating objects in the database easier
def visualTest(request):
    # Delete anything in the database

    for newCourse in Course.objects.all():
        newCourse.delete()

    newCourse = Course.objects.create(pk=1)
    newCourse.setName("CMSC 313")
    newCourse.setSection(1)
    newCourse.setMaxxp(5)


    # Create custom quests with some test values
    # Test Quest 1: using type 1 to give the user questions to answer
    Q = newCourse.quest_set.create(pk=1)
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

    newCourse.save()
    # Test quest 2: A quest manually updated by the admin (Admin functionality not added yet)
    Q = newCourse.quest_set.create(pk=2)
    Q.setName("Test quest 2")
    Q.setDesc("This quest simulates a quest that would be manually updated by the admin, so it will just direct"
              "straight to the summary page")
    Q.setType(0)
    Q.setXP(10)
    Q.setAvailable(True)
    Q.save()

    newCourse.save()

    C = Course.objects.create(pk=2)
    C.setName("New")
    C.save()
    return HttpResponseRedirect(reverse('homepage:menu'))


class mQuestSpecific(generic.DetailView):
    queryset = Quest.objects.all()
    template_name = "homepage/question.html"

    def get_context_data(self, **kwargs):
        context = super(mQuestSpecific, self).get_context_data(**kwargs)
        context['question'] = Question.objects.all()
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

    return HttpResponseRedirect(reverse('homepage:summary', args=(course_id, quest.id,)))


def summary(request, course_id, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    return render(request, 'homepage/summary.html', {'quest': quest})


def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return render(request, 'homepage/profile.html')
