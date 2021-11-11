from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model, login
from django.contrib.auth import authenticate
from django.test import Client

from .models import Course, Quest, Question, Choice


# Create your tests here.

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
