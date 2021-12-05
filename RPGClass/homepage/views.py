from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import Course, Question, Quest, Choice, Skill, Student_course


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


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
    Q.setLives(1)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create(pk=1)
    question.setQuestion("What is the answer to life, the universe, and everything")

    c = question.choice_set.create()
    c.setChoice("Food")
    c.save()
    c = question.choice_set.create()
    c.setChoice("42")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("...what?")
    c.save()

    question.save()
    question = Q.question_set.create(pk=2)
    question.setQuestion("Pineapple on Pizza?")

    c = question.choice_set.create()
    c.setChoice("No")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
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

    C = Course.objects.create(pk=2)
    C.setName("Course 2")
    C.setMaxXP(10)

    Q = C.quest_set.create(pk=3)
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create(pk=3)
    question.setQuestion("What is 10 + 1?")

    c = question.choice_set.create()
    c.setChoice("10")
    c.save()
    c = question.choice_set.create()
    c.setChoice("11")
    c.setCorrect(True)
    c.save()

    question.save()
    question = Q.question_set.create(pk=4)
    question.setQuestion("What is 8 - 2?")

    c = question.choice_set.create()
    c.setChoice("6")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("12")
    c.save()

    question.save()
    Q.save()

    C.save()

    return HttpResponseRedirect(reverse('homepage:menu'))


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


    quest.subHeart()
    quest.save()

    return HttpResponseRedirect(reverse('homepage:summary', args=(course_id, quest.id,)))



def summary(request, course_id, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'homepage/summary.html', {'quest': quest, 'course': course})


def accept(request, course_id, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = quest.getXP()
    request.user.student.addXP(gainedXP)
    request.user.student.save()
    #request.user.student.student_course.addXP(gainedXP)
    request.user.student.save()

    course.updateXP(gainedXP)

    course.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))


def sidequest(request):
    return HttpResponse("Placeholder for the Side Quest page")


def bosses(request):
    return HttpResponse("Placeholder for the Bosses page")


def profile(request):
    return render(request, 'homepage/profile.html')

#def marketplace(request, course_id):
#    return render(request, 'homepage/marketplace.html')

class marketplace(generic.DetailView):
    model = Course
    template_name = 'homepage/marketplace.html'

def create_course_student(request, course_id):
    user = get_object_or_404(User, pk=request.user.id)

    for student_course in user.student.student_course_set.all():
        if (student_course._course_id == course_id):
            student_course.delete()

    user.student.student_course_set.create(student=request.user.student, _course_id=course_id)
    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))

def skillscreate(request, course_id):
    # Delete anything in the database

    course = get_object_or_404(Course, pk=course_id)

    for newSkills in course.skill_set.all():
        newSkills.delete()

    print("this works")

    S = course.skill_set.create(pk=1)
    S.setName("Gain Hearts")
    S.setDesc("You can get one heart")
    S.setCost(200)
    S.save()

    S = course.skill_set.create(pk=2)
    S.setName("Gain Extra time")
    S.setDesc("Gain extra time on a timed quests")
    S.setCost(300)
    S.save()

    S = course.skill_set.create(pk=3)
    S.setName("Gain XP")
    S.setDesc("Boost XP")
    S.setCost(500)
    S.save()

    S = course.skill_set.create(pk=5)
    S.setName("bomb choice")
    S.setDesc("during a multiple choice question, able to eliminate a random choice")
    S.setCost(800)
    S.save()

    S = course.skill_set.create(pk=6)
    S.setName("extra shot")
    S.setDesc("if you get a question wrong, get another shot at it")
    S.setCost(800)
    S.save()

    S = course.skill_set.create(pk=7)
    S.setName("Automatic correct answer")
    S.setDesc("gets an automatic correct answer")
    S.setCost(500)
    S.save()

    course.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))
