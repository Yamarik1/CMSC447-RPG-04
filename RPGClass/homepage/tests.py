from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth import get_user_model, login
from django.contrib.auth import authenticate
from django.test import Client
from selenium.webdriver.common.by import By
from selenium import webdriver

from .models import Course, Quest, Question, Choice

# Create your tests here.

geck_path: str ='/Users/matt/PycharmProjects/CMSC447-RPG-04/RPGClass/homepage/Gecko/geckodriver.exe'

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


# Function to make a Quest with a number of questions, each with a number of Choices. The correct answer is decided
# by a list of integers, this expects the length of the list to be the number of questions, and the integer values need
# to be within 0 and numChoices. Used for larger tests.
def CreateQuest(name, numQuestions, numChoices, rightList=[], testChoice=[]):
    C = Course.objects.create()

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
        C = Course.objects.create()

        url = reverse('homepage:mainquest', args=(C.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no quests available.")

    # Test with 2 quests to test that they will both be listed
    def test_with_quests(self):
        C = Course.objects.create()
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

    # Test that if the quest is specified, it will not be available to the user
    def test_no_quest(self):
        C = Course.objects.create()
        quest = C.quest_set.create()
        quest.setAvailable(False)

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This quest is not available")

    # Test that if a quest should be available, it will be shown on the page
    def test_quest_available(self):
        # Make a quest with basic parameters
        C = Course.objects.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()
        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click here to Start of the quest!")

    # Checks to see if a quest with type zero will give the right pages
    def test_type_quest_0(self):
        C = Course.objects.create()
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
        C = Course.objects.create()
        quest = C.quest_set.create()
        quest.setAvailable(True)
        quest.setType(0)
        quest.setXP(10)
        quest.save()

        url = reverse('homepage:summary', args=(C.id, quest.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Click here to accept the quest results:")


# Create a basic question for some unit tests.
def create_QuestionView_Quest(question="N/A", choice="N/A"):
    C = Course.objects.create()
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


#hearts test but with a server
class hearts_server(LiveServerTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

        #need geckodriver.exe to run firefox. haven't tested it on other browsers
        self.browser = webdriver.Firefox(executable_path=geck_path)

        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        self.user.delete()

    #test if you can actually navigate the server
    def test_server(self):
        #basically "127.0.0.1:8000/accounts/login/" but when using tests, server is not the same
        self.browser.get("%s%s" % (self.live_server_url, reverse('accounts:login')))
        #making sure we are at the right url with the title tab
        assert 'Title' in self.browser.title

    def test_hearts(self):
        #testList = [0]
        #testChoice = ["1", "2", "3"]
        #quest = CreateQuest("Test1", 1, 3, testList, testChoice)
        #quest.setLives(3)

        #hardcoded this from views since the create quest function couldn't reduce lives by 1
        for newCourse in Course.objects.all():
            newCourse.delete()

        newCourse = Course.objects.create(pk=1)
        newCourse.setName("Kaer Morhen")
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
        question.setQuestion("What is the meaning of life")

        c = question.choice_set.create()
        c.setChoice("2B")
        c.save()
        c = question.choice_set.create()
        c.setChoice("to Be")
        c.save()
        c = question.choice_set.create()
        c.setChoice("to be dooby doo")
        c.setCorrect(True)
        c.save()

        question.save()
        Q.save()

        newCourse.save()

        #to get past homepage
        self.client.login(username='test', password='12test12')

        self.browser.get("%s%s" % (self.live_server_url, reverse('homepage:mQuest', args=(newCourse.id, Q.id,))))
        assert 'quest' in self.browser.title

        #finds the button when clicking on a multiple choice answer so we can click it
        radio_button = self.browser.find_element(By.XPATH, "//input[@id='choice1']")
        radio_button.click()
        #get's the submit button so we click it and activate the answer view so that hearts can go down
        element = self.browser.find_element(By.XPATH, "//input[@type='submit']")
        element.click()

        #since the quest we saved in this function is local copy, need the copy that we used to save the new amount of lives in
        quest = get_object_or_404(Quest, pk=Q.id)

        #originally had 3 lives and should be reduced to 2
        self.assertEqual(quest.getLives(), 2)


#testing number of lives
class hearts(TestCase):
    #test if number displays correctly
    def test_correct_lives(self):
        C = Course.objects.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(3)
        quest.save()

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        #makes sure we are at the right page
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        #since we set lives to 3, should output 3
        self.assertContains(response, "number of lives: 3")

    #tests if having no hearts leads to the right page
    def test_no_hearts(self):
        C = Course.objects.create()
        quest = C.quest_set.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.setType(1)
        quest.setLives(0)
        quest.save()

        url = reverse('homepage:mQuestView', args=(C.id, quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        #the page should be different and tells you you cannot do quest
        self.assertContains(response, "you are out of lives")


class courseTests(TestCase):

    # function to make a test course
    def makeClass(self):
        C = Course.objects.create()
        C.save()
        return C

    # Test that multiple quests can be seen on the class page
    def test_class_list(self):
        C1 = self.makeClass()
        C1.setName("Course 1")
        C1.save()

        C2 = self.makeClass()
        C2.setName("Course 2")
        C2.save()

        url = reverse('homepage:course')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, C1.getName())
        self.assertContains(response, C2.getName())

    # Test that will make sure that levels are being found properly, and that it is being shown to the user correctly
    def test_level_value(self):
        C = self.makeClass()
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
        C = self.makeClass()

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
        C1 = self.makeClass()
        C1.setMaxXP(5)
        C1.updateXP(7)
        C1.save()

        C2 = self.makeClass()
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

