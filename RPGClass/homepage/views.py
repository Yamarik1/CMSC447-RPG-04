from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Course, Quest, SideQuest, Boss, Recs, Student_course, Course_General
from accounts.models import Student


# prevents people from seeing page until they login in (generic and not assinged to a specific course)

@login_required(login_url="/accounts/login/")
def homepage(request):
    return render(request, 'homepage/menu.html')


class course(generic.ListView):
    template_name = 'homepage/course.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        currUser = self.request.user
        currStudent = Student.objects.get(user=currUser)
        currStudentC = Student_course.objects.get(student=currStudent)
        return currStudentC.course_set.all()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_id'] = self.kwargs['course_id']
        return context


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
    user = request.user
    student = Student.objects.get(user=user)
    stuC = Student_course.objects.get(student=student)
    quest = get_object_or_404(Quest, pk=quest_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = quest.getXP()
    # XP for the course will get updated after the accept button is chosen.
    course.updateXP(gainedXP)
    stuC.updateXP(gainedXP)

    course.save()
    stuC.save()

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
    user = request.user
    student = Student.objects.get(user=user)
    stuC = Student_course.objects.get(student=student)
    sidequest = get_object_or_404(SideQuest, pk=sidequest_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = sidequest.getXP()

    course.updateXP(gainedXP)
    stuC.updateXP(gainedXP)

    course.save()
    stuC.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))


def profile(request):
    user = request.user
    print(user.username)
    stu = Student.objects.get(user=user)
    print(stu.getStudentName())
    student = Student_course.objects.get(student=stu)
    print(student.getXP())
    return render(request, 'homepage/profile.html', {'currstudent': student})

class profileSpecific(generic.DetailView):
    model = Course
    template_name='homepage/profileS.html'


class leaderboard(generic.ListView):
    template_name = 'homepage/leaderboard.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        currUser = self.request.user
        currStudent = Student.objects.get(user=currUser)
        currStudentC = Student_course.objects.get(student=currStudent)

        currCourse = Course.objects.get(pk=self.kwargs['course_id'])

        ID = currCourse.getCourseID()


        for course in Course_General.objects.all():

            if course.getCourseID() == ID:

                list = course.student_course_set.all()

                return list.order_by('-_curr_XP')


def accountTest(request):
    # Delete anything in the database
    # for userd in User.objects.all():
    # userd.delete()

    user = request.user
    student = Student(pk=1, user=user)
    student.setStudentName('test')
    student.save()

    courseStu = Student_course(student=student)
    courseStu.setXP(0)
    courseStu.setName('test')

    courseStu.save()

    user1 = User.objects.create_user(username='MasterChief', password='12test12')
    user1.save()

    student = Student(pk=2, user=user1)
    student.setStudentName('MasterChief')
    student.save()

    courseStu = Student_course(student=student)
    courseStu.setXP(14)
    courseStu.setName('MasterChief')

    courseStu.save()

    user2 = User.objects.create_user(username='TacoCat', password='12test12')
    user2.save()

    student = Student(pk=3, user=user2)
    student.setStudentName('TacoCat')
    student.save()

    courseStu = Student_course(student=student)
    courseStu.setXP(45)
    courseStu.setName('TacoCat')
    courseStu.save()

    return HttpResponseRedirect(reverse('homepage:menu'))


def courseIni(request):
    courseS = Course_General.objects.create(pk=1)
    courseS.setCourseID(100001)
    courseS.setName("Fus Ro Dah")
    courseS.save()

    courseS = Course_General.objects.create(pk=2)
    courseS.setCourseID(100002)
    courseS.setName("Course 2")
    courseS.save()

    return HttpResponseRedirect(reverse('homepage:menu'))


# For the purposes of creating objects in the database easier
def visualTest(request):
    currUser = User.objects.get(pk=1)
    currStudent = Student.objects.get(user=currUser)
    currStudentC = Student_course.objects.get(student=currStudent)

    currStudentC.course_general.add(Course_General.objects.get(pk=1))
    currStudentC.course_general.add(Course_General.objects.get(pk=2))

    for newCourse in currStudentC.course_set.all():
        newCourse.delete()

    newCourse = currStudentC.course_set.create()
    newCourse.setName("Fus Ro Dah")
    newCourse.setSection(1)
    newCourse.setMaxXP(5)
    newCourse.setCourseID(100001)

    # Create custom quests with some test values
    # Test Quest 1: using type 1 to give the user questions to answer
    Q = newCourse.quest_set.create()
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create()
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
    question = Q.question_set.create()
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
    Q = newCourse.quest_set.create()
    Q.setName("Test quest 2")
    Q.setDesc("This quest simulates a quest that would be manually updated by the admin, so it will just direct"
              "straight to the summary page")
    Q.setType(0)
    Q.setXP(7)
    Q.setAvailable(True)
    Q.save()

    # Set up the bosses database table

    # Create custom boss with some test values
    # Test Boss 1: using type 1 to give the user questions to answer

    Q = newCourse.boss_set.create()
    Q.setName("Boss 1")
    Q.setDesc("This is the first test Boss")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    # Creates Questions, choices and answers for the bosses
    question = Q.question_set.create()
    question.setQuestion("What is 1 + 1")

    c = question.choice_set.create()
    c.setChoice("2")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("13")
    c.save()

    question.save()
    question = Q.question_set.create()
    question.setQuestion("What is 10 - 2?")

    c = question.choice_set.create()
    c.setChoice("8")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("12")
    c.save()

    question.save()

    question = Q.question_set.create()
    question.setQuestion("What is the spelling for the word wrong?")

    c = question.choice_set.create()
    c.setChoice("wrong")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("right")
    c.save()
    question.save()

    Q.save()

    newCourse.save()
    # Set up the recommended topics visual test

    # Create custom recommendation with some test values
    # Test recs 1 named recommended topics:
    Q = newCourse.recs_set.create()
    Q.setName("Recommended Topics")

    # Creates topics
    topic = Q.topic_set.create()
    topic.setTopic("Scoreboards")
    topic.save()

    topic = Q.topic_set.create()
    topic.setTopic("Circuts")
    topic.save()

    Q.save()

    newCourse.save()

    squest = newCourse.sidequest_set.create()
    squest.setName("Side Quest 1")
    squest.setType(1)
    squest.setLives(5)
    squest.setAvailable(True)

    question = squest.question_set.create()
    question.setQuestion("test")
    question.save()
    c = question.choice_set.create()
    c.setChoice("Right")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("Wrong")
    c.save()
    squest.save()
    newCourse.save()

    C = currStudentC.course_set.create()
    C.setName("Course 2")
    C.setMaxXP(10)
    C.setCourseID(100002)

    Q = C.quest_set.create()
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create()
    question.setQuestion("What is 10 + 1?")

    c = question.choice_set.create()
    c.setChoice("10")
    c.save()
    c = question.choice_set.create()
    c.setChoice("11")
    c.setCorrect(True)
    c.save()

    question.save()
    question = Q.question_set.create()
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

    ##########
    # Create courses for second user

    currUser = User.objects.get(pk=2)
    currStudent = Student.objects.get(user=currUser)
    currStudentC = Student_course.objects.get(student=currStudent)

    currStudentC.course_general.add(Course_General.objects.get(pk=1))

    for newCourse in currStudentC.course_set.all():
        newCourse.delete()

    newCourse = currStudentC.course_set.create()
    newCourse.setName("Fus Ro Dah")
    newCourse.setSection(1)
    newCourse.setMaxXP(5)
    newCourse.setCourseID(100001)

    # Create custom quests with some test values
    # Test Quest 1: using type 1 to give the user questions to answer
    Q = newCourse.quest_set.create()
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create()
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
    question = Q.question_set.create()
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
    Q = newCourse.quest_set.create()
    Q.setName("Test quest 2")
    Q.setDesc("This quest simulates a quest that would be manually updated by the admin, so it will just direct"
              "straight to the summary page")
    Q.setType(0)
    Q.setXP(7)
    Q.setAvailable(True)
    Q.save()

    # Set up the bosses database table

    # Create custom boss with some test values
    # Test Boss 1: using type 1 to give the user questions to answer

    Q = newCourse.boss_set.create()
    Q.setName("Boss 1")
    Q.setDesc("This is the first test Boss")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    # Creates Questions, choices and answers for the bosses
    question = Q.question_set.create()
    question.setQuestion("What is 1 + 1")

    c = question.choice_set.create()
    c.setChoice("2")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("13")
    c.save()

    question.save()
    question = Q.question_set.create()
    question.setQuestion("What is 10 - 2?")

    c = question.choice_set.create()
    c.setChoice("8")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("12")
    c.save()

    question.save()

    question = Q.question_set.create()
    question.setQuestion("What is the spelling for the word wrong?")

    c = question.choice_set.create()
    c.setChoice("wrong")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("right")
    c.save()
    question.save()

    Q.save()

    newCourse.save()
    # Set up the recommended topics visual test

    # Create custom recommendation with some test values
    # Test recs 1 named recommended topics:
    Q = newCourse.recs_set.create()
    Q.setName("Recommended Topics")

    # Creates topics
    topic = Q.topic_set.create()
    topic.setTopic("Scoreboards")
    topic.save()

    topic = Q.topic_set.create()
    topic.setTopic("Circuts")
    topic.save()

    Q.save()

    newCourse.save()

    squest = newCourse.sidequest_set.create()
    squest.setName("Side Quest 1")
    squest.setType(1)
    squest.setLives(5)
    squest.setAvailable(True)

    question = squest.question_set.create()
    question.setQuestion("test")
    question.save()
    c = question.choice_set.create()
    c.setChoice("Right")
    c.setCorrect(True)
    c.save()
    c = question.choice_set.create()
    c.setChoice("Wrong")
    c.save()
    squest.save()
    newCourse.save()

    currUser = User.objects.get(pk=3)
    currStudent = Student.objects.get(user=currUser)
    currStudentC = Student_course.objects.get(student=currStudent)

    currStudentC.course_general.add(Course_General.objects.get(pk=2))

    C = currStudentC.course_set.create()
    C.setName("Course 2")
    C.setMaxXP(10)
    C.setCourseID(100002)

    Q = C.quest_set.create()
    Q.setName("Quest 1")
    Q.setDesc("This is the first test quest")
    Q.setLives(3)
    Q.setAvailable(True)
    Q.setType(1)

    question = Q.question_set.create()
    question.setQuestion("What is 10 + 1?")

    c = question.choice_set.create()
    c.setChoice("10")
    c.save()
    c = question.choice_set.create()
    c.setChoice("11")
    c.setCorrect(True)
    c.save()
    Q.save()
    C.save()
    currStudentC.save()

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
    questionSet = boss.question_set.all()

    # The choice will be check for each question, and the correct counter will increment if the right answer is chosen.
    for question in questionSet:

        selected_choice = question.choice_set.get(pk=request.POST[question.getQuestion()])

        if selected_choice.getCorrect():
            boss.rightAnsChosen()
            boss.save()
            selected_choice.save()

    boss.subHeart()
    boss.save()

    return HttpResponseRedirect(reverse('homepage:bossSummary', args=(course_id, boss_id,)))


def bossSummary(request, course_id, boss_id):
    boss = get_object_or_404(Boss, pk=boss_id)
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'homepage/bossSummary.html', {'boss': boss, 'course': course})


def bAccept(request, course_id, boss_id):
    user = request.user
    student = Student.objects.get(user=user)
    stuC = Student_course.objects.get(student=student)
    boss = get_object_or_404(Boss, pk=boss_id)
    course = get_object_or_404(Course, pk=course_id)

    gainedXP = boss.getXP()

    course.updateXP(gainedXP)
    stuC.updateXP(gainedXP)

    course.save()
    stuC.save()

    return HttpResponseRedirect(reverse('homepage:courseS', args=(course_id,)))
