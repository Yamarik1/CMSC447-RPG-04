from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth import get_user_model, login
from django.contrib.auth import authenticate
from django.test import Client
from selenium.webdriver.common.by import By
from selenium import webdriver


from .models import Course_General, Student_courseList, Course, Quest, Question, Choice, Boss, Recs, Topic, Skill, bossDate, Date, Improve, ImproveTopic, Student_course
from accounts.models import Student


# Create your tests here.

geck_path: str = '/Users/matt/PycharmProjects/CMSC447-RPG-04/RPGClass/homepage/Gecko/geckodriver.exe'


# Test for the skeleton homepage
class TestHomepage(TestCase):
    # The homepage needs an account to reach, so here the account is made
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_url_correctness(self):
        self.client.login(username='test', password='12test12')

        response = self.client.get(reverse('homepage:menu'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to RPG Class!")


def create_user():
    C = Client()
    user = get_user_model().objects.create_user(username='test', password='12test12')
    C.force_login(user)

    student = Student(pk=1, user=user)
    student.setStudentName("test")
    student.save()

    studentC = Student_course(pk=1, student=student)
    studentC.save()

    courseStu = Student_courseList(pk=1, student=student)
    courseStu.save()
    return courseStu


# Function to make a Quest with a number of questions, each with a number of Choices. The correct answer is decided
# by a list of integers, this expects the length of the list to be the number of questions, and the integer values need
# to be within 0 and numChoices. Used for larger tests.
def CreateQuest(name, numQuestions, numChoices, rightList=[], testChoice=[]):
    user = create_user()

    C = user.course_set.create()

    testQuest = C.quest_set.create()
    testQuest.setName(name)
    testQuest.setType(1)

    for i in range(numQuestions):
        q = testQuest.question_set.create()

        for j in range(numChoices):
            c = q.choice_set.create()
            if rightList[i] == j:
                c.setCorrect(True)
                c.setChoice(testChoice[j])
                c.save()

            else:
                c.setCorrect(False)
                c.setChoice(testChoice[j])
                c.save()

        q.save()
    testQuest.save()

    return testQuest


class TestQuestMethods(TestCase):

    # Test getters and setters
    def test_quest_getters_and_setters(self):

        # Create a test question using some basic values
        quest = CreateQuest("Test", 1, 1, [1], [1])
        isWorking = True

        # Question name
        quest.setName("Question 1")
        if quest.getName() != "Question 1":
            isWorking = False

        # Question description
        quest.setDesc("This is the first Question")
        if quest.getDesc() != "This is the first Question":
            isWorking = False

        # Question Lives
        quest.setLives(3)
        if quest.getLives() != 3:
            isWorking = False

        self.assertIs(isWorking, True)


# Test class to test the general view of the quest list
class TestQuestList(TestCase):

    # Test that if no quests exist in a course, the proper message is given
    def test_no_quests(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()

        url = reverse('homepage:mainquest', args=(C.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no quests available.")

    # Test with 2 quests to test that they will both be listed
    def test_with_quests(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        Q = C.quest_set.create()

        Q.setName("Quest 1")
        Q.save()

        Q = C.quest_set.create()
        Q.setName("Quest 2")
        Q.save()

        url = reverse('homepage:mainquest', args=(C.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quest 1")
        self.assertContains(response, "Quest 2")


class TestQuest(TestCase):

    # Test that correct answers can be assigned and identified
    def test_correct_choice(self):

        # Counter keeps track of which pk should be used for choices
        counter = 1
        testList = [0, 1, 2]
        testChoice = ["1", "2", "3"]
        answerArray = [False, False, False]
        counter = 1
        quest = CreateQuest("Test1", 3, 3, testList, testChoice)
        for i in range(1, 4):

            q = quest.question_set.get(pk=i)

            for j in range(1, 4):

                c = q.choice_set.get(pk=counter)
                # Once a correct answer is found, the entry in the list changes to True
                if c.getCorrect():
                    answerArray[i - 1] = True
                counter += 1
        # Test fails if there is any false in the list, thus no correct answer is chosen
        self.assertIs(False in answerArray, False)


# Test views
class QuestViewTest(TestCase):

    def makeClass(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        C.save()
        C.setName("Course1")
        return C

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='test', password='12test12')
        self.client.login(username='test', password='12test12')
        C = self.makeClass()
        self.client.post(reverse('homepage:skill_in', args=(C.id,)))
        self.client.post(reverse('homepage:course_student', args=(C.id,)))
        self.user.save()

    # deletes user
    def tearDown(self):
        self.user.delete()

    # Test that if the quest is specified, it will not be available to the user
    def test_no_quest(self):
        user = Student_courseList.objects.create()
        student = Student_course.objects.create()
        student.save()
        C = student.course_set.create()
        C.save

        quest = C.quest_set.create()
        quest.setAvailable(False)

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This quest is not available")

    # Test that if a quest should be available, it will be shown on the page
    def test_quest_available(self):
        # Make a quest with basic parameters
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()
        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click here to Start the quest!")

    # Checks to see if a quest with type zero will give the right pages
    def test_type_quest_0(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.quest_set.create()
        quest.setAvailable(True)
        quest.setType(0)
        quest.setXP(10)
        quest.setLives(3)
        quest.save()

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        # Test that the proper message is displayed and the specific quest screen
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This quest doesn't have anymore work for you to do!")

        # Test that Type 0 quests will present a proper summary page with proper XP value
        url = reverse('homepage:summary', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "XP gained: " + str(quest.getXP()))

    # With the summary page being updated, this test makes sure the summary page appears with the new info
    def test_summary_page(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.quest_set.create()
        quest.setAvailable(True)
        quest.setType(0)
        quest.setLives(1)
        quest.setXP(10)
        quest.save()

        url = reverse('homepage:summary', args=(C.id, quest.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click here to accept the quest results:")


# Create a basic question for some unit tests.
def create_QuestionView_Quest(question="N/A", choice="N/A"):
    user = Student_courseList.objects.create()
    C = user.course_set.create()
    quest = C.quest_set.create()
    quest.setType(1)
    quest.setAvailable(True)
    question = quest.question_set.create()
    question.setQuestion(question)

    if (choice != "N/A"):
        choice = question.choice_set.create()
        choice.setChoice(choice)

    quest.save()
    C.save()
    return C


class QuestionsViewTest(TestCase):

    def makeClass(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        C.save()
        C.setName("Course1")
        return C

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='test', password='12test12')
        self.client.login(username='test', password='12test12')
        C = self.makeClass()
        self.client.post(reverse('homepage:skill_in', args=(C.id,)))
        self.client.post(reverse('homepage:course_student', args=(C.id,)))
        self.user.save()

    # deletes user
    def tearDown(self):
        self.user.delete()

    # Test to make sure a question with no choices presents the proper message on the page
    def test_question_with_no_choices(self):
        # Test that a single question with no choices presents the proper page
        C = create_QuestionView_Quest("TestQuestion")
        quest = C.quest_set.get(pk=1)
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This Question does not have any choices")

    # Test that one question can be properly be displayed on the page
    def test_1_question(self):
        # Test that a single question produces its proper page
        C = create_QuestionView_Quest("Test Question", "Test Choice")
        quest = C.quest_set.get(pk=1)
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.choice_set.get(pk=1).getChoice())

    # Test the multiple questions can be presented on the page
    def test_2_questions(self):
        C = create_QuestionView_Quest("Test Question", "Test Choice")
        quest = C.quest_set.get(pk=1)
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.choice_set.get(pk=1).getChoice())

        question2 = quest.question_set.create()
        question2.setQuestion("Test Question 2")

        choice2 = question2.choice_set.create()
        choice2.setChoice("Test Choice 2")

        url = reverse('homepage:mQuest', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question2.choice_set.get(pk=2).getChoice())

    # Test one question with choices, and one without
    def test_mixed_questions(self):
        C = create_QuestionView_Quest("Test Question", "Test Choice")
        quest = C.quest_set.get(pk=1)
        question = quest.question_set.get(pk=1)

        question2 = quest.question_set.create()
        question2.setQuestion("Test Question 2")
        question2.save()

        url = reverse('homepage:mQuest', args=(C.id, quest.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Question")
        self.assertContains(response, "This Question does not have any choices")


# Function to test the creation of a boss with certain number of questions, choices and answers
def CreateBoss(name, numQuestions, numChoices, rightList=[], testChoice=[]):
    user = Student_courseList.objects.create()
    C = user.course_set.create()
    testBoss = C.boss_set.create()
    testBoss.setName(name)
    testBoss.setType(1)

    for i in range(numQuestions):
        q = testBoss.question_set.create()

        for j in range(numChoices):
            c = q.choice_set.create()
            if rightList[i] == j:
                c.setCorrect(True)
                c.setChoice(testChoice[j])
                c.save()

            else:
                c.setCorrect(False)
                c.setChoice(testChoice[j])
                c.save()

        q.save()
    testBoss.save()
    C.save()
    return C


# Tests the boss methods
class TestBossMethods(TestCase):

    # Test getters and setters
    def test_boss_getters_and_setters(self):

        # Create a test question using some basic values

        newcourse = CreateBoss("Test", 1, 1, [1], [1])
        isWorking = True

        # Question name
        boss = newcourse.boss_set.get(pk=1)
        boss.setName("Question 1")
        if boss.getName() != "Question 1":
            isWorking = False

        # Question description
        boss.setDesc("This is the first Question")
        if boss.getDesc() != "This is the first Question":
            isWorking = False

        # Question Lives
        boss.setLives(3)
        if boss.getLives() != 3:
            isWorking = False

        self.assertIs(isWorking, True)


# Test boss views
class BossViewTest(TestCase):

    # Test that if the boss is specified, it will not be available to the user
    def test_no_boss(self):
        user = Student_courseList.objects.create()
        newcourse = user.course_set.create()
        boss = newcourse.boss_set.create()
        boss.setAvailable(False)
        boss.save()
        newcourse.save()
        url = reverse('homepage:bossView', args=(newcourse.id, boss.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This boss is not yet available")

    # Test that if a quest should be available, it will be shown on the page
    def test_boss_available(self):
        # Make a quest with basic parameters
        user = Student_courseList.objects.create()
        newcourse = user.course_set.create()
        boss = newcourse.boss_set.create()
        boss.setName("Test Boss")
        boss.setAvailable(True)
        boss.setType(1)
        boss.setLives(1)
        boss.save()
        newcourse.save()

        url = reverse('homepage:bossView', args=(newcourse.id, boss.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click here to Start the boss!")

    # Checks to see if a boss with type zero will give the right pages
    def test_type_quest_0(self):
        user = Student_courseList.objects.create()
        newcourse = user.course_set.create()
        boss = newcourse.boss_set.create()
        boss.setAvailable(True)
        boss.setType(0)
        boss.setLives(1)
        boss.setXP(10)
        boss.save()
        newcourse.save()
        url = reverse('homepage:bossView', args=(newcourse.id, boss.id,))

        # Test that the proper message is displayed and the specific quest screen
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This boss has already been attacked!")

    # Test to make sure the summary page shows the proper XP value
    def test_boss_XP(self):
        user = Student_courseList.objects.create()
        newcourse = user.course_set.create()
        boss = newcourse.boss_set.create()
        boss.setAvailable(True)
        boss.setType(1)
        boss.setLives(1)
        boss.setXP(10)
        boss.save()
        newcourse.save()
        url = reverse('homepage:bossSummary', args=(newcourse.id, boss.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "XP gained: 10")


# Create a basic question for bosses
def create_QuestionView_Boss(question="N/A", choice="N/A"):
    boss = Boss.objects.create()
    boss.setType(1)
    boss.setAvailable(True)
    question = boss.question_set.create()
    question.setQuestion(question)

    if (choice != "N/A"):
        choice = boss.choice_set.create()
        choice.setChoice(choice)

    boss.save()
    return boss


# Tests the creation of topics and recommendations
def recsTest(topics="yes"):
    # Create custom recommendation with some test values
    # Test recs 1 named recommended topics:
    rec = Recs.objects.create()
    rec.setAvailable(True)
    topic = rec.topic_set.create()
    topic.setTopic(topics)

    rec.save()

    return rec


# Tests the creation of improve topics
def improveTest(topics="yes"):
    # Create custom improve list with some test values
    # Test improve 1:
    improv = Improve.objects.create()
    improv.setAvailable(True)
    improvetopic = improv.improvetopic_set.create()
    improvetopic.setTopic(topics)

    improv.save()

    return improv

#testing number of lives
class hearts(TestCase):
    #test if number displays correctly
    def makeClass(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        C.save()
        C.setName("Course1")
        return C

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='test', password='12test12')
        self.client.login(username='test', password='12test12')
        C = self.makeClass()
        self.client.post(reverse('homepage:skill_in', args=(C.id,)))
        self.client.post(reverse('homepage:course_student', args=(C.id,)))
        self.user.save()

    # deletes user
    def tearDown(self):
        self.user.delete()


    def test_correct_lives(self):
        #curruser = Student(user=self.user)
        #s = Student_course(student=curruser)

        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        # makes sure we are at the right page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # since we set lives to 3, should output 3
        self.assertContains(response, "number of lives: 3")

    # tests if having no hearts leads to the right page
    def test_no_hearts(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(0)
        quest.save()

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # the page should be different and tells you you cannot do quest
        self.assertContains(response, "you are out of lives")

    def test_sidequest_lives(self):
        user = Student_courseList.objects.create()
        studentC = Student_course.objects.create()




        C = user.course_set.create()
        #D = studentC.course_set.create()

        quest = C.sidequest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()

        url = reverse('homepage:sQuestView', args=(C.id, quest.id,))

        # makes sure we are at the right page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # since we set lives to 3, should output 3
        self.assertContains(response, "number of lives: 3")

    def test_boss_lives(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        quest = C.boss_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()

        url = reverse('homepage:bossView', args=(C.id, quest.id,))

        # makes sure we are at the right page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # since we set lives to 3, should output 3
        self.assertContains(response, "Number of lives remaining: 3")


class CourseTests(TestCase):

    # function to make a test course
    def makeClass(self, user):
        C = user.course_set.create()
        C.save()
        return C

    # Test that will make sure that levels are being found properly, and that it is being shown to the user correctly
    def test_level_value(self):
        user = Student_courseList.objects.create()
        C = self.makeClass(user)
        # Set the value of needed XP to 5, and the current XP had is 7, so the level should increase by 1
        C.setMaxXP(5)

        C.updateXP(7)
        C.save()
        url = reverse('homepage:courseS', args=(1,))

        response = self.client.get(url)
        # At current Xp of 7, the level should be 2, Total should be 7, and xp to next level should be 3
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current Level: 2")
        self.assertContains(response, "Total XP earned: 7")
        self.assertContains(response, "Xp to next level: 3")

    # Test to simulate multiple different quests still allow course to get correct level
    def test_multiple_quests(self):
        user = Student_courseList.objects.create()
        C = self.makeClass(user)

        C.setMaxXP(5)

        Q1 = C.quest_set.create()
        Q1.setXP(5)
        Q1.save()
        C.updateXP(Q1.getXP())

        Q2 = C.quest_set.create()
        Q2.setXP(7)
        Q2.save()
        C.updateXP(Q2.getXP())

        C.save()

        url = reverse('homepage:courseS', args=(1,))

        response = self.client.get(url)
        # At current Xp of 12, the level should be 3, Total should be 12, and xp to next level should be 3
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current Level: 3")
        self.assertContains(response, "Total XP earned: 12")
        self.assertContains(response, "Xp to next level: 3")

    # Test the correctness of multiple courses being defined
    def test_multiple_courses(self):
        user = Student_courseList.objects.create()
        C1 = self.makeClass(user)
        C1.setMaxXP(5)
        C1.updateXP(7)
        C1.save()

        C2 = self.makeClass(user)
        C2.setMaxXP(10)
        C2.updateXP(29)
        C2.save()

        # Test the pages with the XP values on them
        # The first set will be Level 2, Total Xp is 7, To next is 3
        url = reverse('homepage:courseS', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current Level: 2")
        self.assertContains(response, "Total XP earned: 7")
        self.assertContains(response, "Xp to next level: 3")

        # Second set will pass in the args of 2, since it need to check the second quest
        # Level will be 3, Total XP is 29, To next is 1
        url = reverse('homepage:courseS', args=(2,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Current Level: 3")
        self.assertContains(response, "Total XP earned: 29")
        self.assertContains(response, "Xp to next level: 1")



class SkillTest(TestCase):

    def makeClass(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        C.save()
        C.setName("Course1")
        return C

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='test', password='12test12')
        self.client.login(username='test', password='12test12')
        C = self.makeClass()
        self.client.post(reverse('homepage:skill_in', args=(C.id,)))
        self.client.post(reverse('homepage:course_student', args=(C.id,)))
        self.user.save()

    # deletes user
    def tearDown(self):
        self.user.delete()

    def test_creating_skills_for_players(self):
        student = self.user.student.student_course_set.first()
        self.assertEqual(self.user.student.student_course_set.count(), 1)
        self.assertEqual(len(student.skills), 6)

    def test_marketplace(self):
        url = reverse('homepage:marketplace', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "gainHearts 0")
        self.assertContains(response, "your Money: 1000")

        #bassically what view is doing when posting (aka buying a skill). couldn't figure out posting with data
        skill = Skill.objects.filter(_id='gainHearts').first()
        student = self.user.student.student_course_set.first()
        student.setCoins(student.getCoins() - skill.getCost())
        student.skills[skill.getId()] += 1
        student.save()

        response = self.client.get(url)
        self.assertContains(response, "your Money: 800")
        self.assertContains(response, "gainHearts 1")

    def test_course_profile(self):
        url = reverse('homepage:course_profile', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Quests")
        self.assertContains(response, "gainHearts 0")
        self.assertContains(response, "Course Info")


# Add additional tests for the side quests
class sideQuest(TestCase):

    def makeClass(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        C.save()
        C.setName("Course1")
        return C

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username='test', password='12test12')
        self.client.login(username='test', password='12test12')
        C = self.makeClass()
        self.client.post(reverse('homepage:skill_in', args=(C.id,)))
        self.client.post(reverse('homepage:course_student', args=(C.id,)))
        self.user.save()

    # deletes user
    def tearDown(self):
        self.user.delete()

    # Makes sure the side quest page exists
    def test_sidequest_page(self):
        user = Student_courseList.objects.create()
        course = user.course_set.create()
        course.save()

        url = reverse('homepage:sidequest', args=(1,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Side Quests")

    # Makes sure the sidequest can appear on the sidequest page
    def test_sidequest_list(self):
        user = Student_courseList.objects.create()
        course = user.course_set.create()
        course.save()

        sQuest = course.sidequest_set.create()
        sQuest.setName("Side Quest 1")

        sQuest.save()
        sQuest = course.sidequest_set.create()
        sQuest.setName("Side Quest 2")

        url = reverse('homepage:sidequest', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, course.sidequest_set.get(pk=1).getName())
        self.assertContains(response, course.sidequest_set.get(pk=2).getName())

    # Test the sidequest page to make sure a type 0 sidequest will give the proper message
    def test_sidequest_specific_type_0(self):
        user = Student_courseList.objects.create()
        course = user.course_set.create()
        course.save()

        sidequest = course.sidequest_set.create()
        sidequest.setName("sidequest 1")
        sidequest.setAvailable(True)
        sidequest.setType(0)
        sidequest.setLives(1)
        sidequest.setXP(10)
        sidequest.save()

        url = reverse('homepage:sQuestView', args=(1, 1))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This quest doesn't have anymore work for you to do!")

    # Test type 1 quest to make sure questions can be printed to the user
    def test_sidequest_question(self):
        user = Student_courseList.objects.create()
        course = user.course_set.create()
        course.save()

        sQuest = course.sidequest_set.create()
        sQuest.setName("Side Quest 1")
        sQuest.setType(1)
        sQuest.setLives(1)

        question = sQuest.question_set.create()
        question.setQuestion("question 1")

        choice = question.choice_set.create()
        choice.setChoice("choice 1")

        choice.save()
        question.save()
        sQuest.save()
        course.save()

        url = reverse('homepage:sQuest', args=(1, 1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "question 1")
        self.assertContains(response, "choice 1")

    # Tests that the summary page is correctly produced
    def test_sidequest_summary(self):
        user = Student_courseList.objects.create()
        C = user.course_set.create()
        squest = C.sidequest_set.create()
        squest.setName("sidequest 1")
        squest.setType(0)
        squest.setAvailable(True)
        squest.setXP(10)

        squest.save()
        C.save()
        url = reverse('homepage:sQuestSummary', args=(1, 1))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "XP gained: 10")


# Tests the leaderboard function
class Leaderboard(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    # Create a user and course, but dont add the user to the course, so the proper page should appear
    def test_no_user(self):
        self.client.login(username='test', password='12test12')
        self.user = User.objects.get(username='test')
        stu = Student(pk=1, user=self.user)
        stu.save()
        user = Student_courseList(pk=1, student=stu)
        user.save()

        course = Course_General.objects.create()
        course.setCourseID(1)
        course.save()

        user.setName("test")
        user.setXP(10)

        C = user.course_set.create()
        C.setCourseID(1)
        C.save()

        url = reverse('homepage:leaderboard', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no valid Users in this class")

    # Create a user and course, add the user to the course, and then check to see the proper name and XP is being
    # printed.
    def test_single_user(self):
        self.client.login(username='test', password='12test12')
        self.user = User.objects.get(username='test')
        stu = Student(pk=1, user=self.user)
        stu.save()
        user = Student_courseList(pk=1, student=stu)
        user.save()

        course = Course_General.objects.create()
        course.setCourseID(1)
        course.save()

        user.setName("test")
        user.setXP(10)

        user.course_general.add(Course_General.objects.get(pk=1))
        user.save()

        C = user.course_set.create()
        C.setCourseID(1)
        C.save()

        url = reverse('homepage:leaderboard', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test : 10")

    # Will add 2 students to a course, then check the leaderboard to see if it is correct
    def test_multiple_users(self):
        self.client.login(username='test', password='12test12')
        self.user = User.objects.get(username='test')

        user2 = get_user_model().objects.create_user(username='test2', password='12test12')
        user2.save()

        stu = Student(pk=1, user=self.user)
        stu.save()
        user = Student_courseList(pk=1, student=stu)
        user.save()

        course = Course_General.objects.create()
        course.setCourseID(1)
        course.save()

        user.setName("test")
        user.setXP(10)

        user.course_general.add(Course_General.objects.get(pk=1))
        user.save()

        C = user.course_set.create()
        C.setCourseID(1)
        C.save()

        stu = Student(pk=2, user=user2)
        stu.save()
        user = Student_courseList(pk=2, student=stu)
        user.save()

        course = Course_General.objects.create()
        course.setCourseID(1)
        course.save()

        user.setName("test2")
        user.setXP(15)

        user.course_general.add(Course_General.objects.get(pk=1))
        user.save()

        C = user.course_set.create()
        C.setCourseID(1)
        C.save()

        url = reverse('homepage:leaderboard', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Tests the exact layout of the page
        self.assertContains(response, "test2 : 15")
        self.assertContains(response, "test : 10")

    # Tests two users, each who are added to separate classes, and check each individual leaderboard
    def test_separate_classes(self):
        self.client.login(username='test', password='12test12')
        self.user = User.objects.get(username='test')

        user2 = get_user_model().objects.create_user(username='test2', password='12test12')
        user2.save()

        stu = Student(pk=1, user=self.user)
        stu.save()
        user = Student_courseList(pk=1, student=stu)
        user.save()

        course = Course_General.objects.create()
        course.setCourseID(1)
        course.save()

        user.setName("test")
        user.setXP(10)

        user.course_general.add(Course_General.objects.get(pk=1))
        user.save()

        C = user.course_set.create()
        C.setCourseID(1)
        C.save()

        course = Course_General.objects.create()
        course.setCourseID(2)
        course.save()

        stu = Student(pk=2, user=user2)
        stu.save()

        user = Student_courseList(pk=2, student=stu)
        user.save()

        user.setName("test2")
        user.setXP(15)

        user.course_general.add(Course_General.objects.get(pk=2))
        user.save()

        C = user.course_set.create()
        C.setCourseID(2)
        C.save()

        url = reverse('homepage:leaderboard', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Tests the first course with the first user
        self.assertContains(response, "test : 10")

        url = reverse('homepage:leaderboard', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Tests the second course with the second user
        self.assertContains(response, "test2 : 15")



