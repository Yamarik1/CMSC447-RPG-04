from django.test import TestCase
from django.urls import reverse

from .models import Quest, Question, Choice


# Create your tests here.

# Test for the skeleton homepage
class TestClass(TestCase):
    # The url found at homepage/menu.html should exist, and will return 200 code
    def test_url_correctness(self):
        response = self.client.get(reverse('homepage:menu'))
        self.assertEqual(response.status_code, 200)

# Test for the main quest homepage
class Quest_test_Class(TestCase):
    # The url found at homepage/mainquest should exist, and will return 200 code
    def test_url_correctness(self):
        response = self.client.get('/homepage/mainquest')
        self.assertEqual(response.status_code, 200)


# Function to make a Quest with a number of questions, each with a number of Choices. The correct answer is decided
# by a list of integers, this expects the length of the list to be the number of questions, and the integer values need
# to be within 0 and numChoices.
def CreateQuest(name, numQuestions, numChoices, rightList=[], testChoice=[]):
    testQuest = Quest.objects.create()
    testQuest.setName(name)

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
    def test_question_getters_and_setters(self):

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


class MainQuest(TestCase):

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

    # Test that if the quest is specified to, it will not be available to the user
    def test_no_quest(self):
        quest = Quest.objects.create()
        quest.setAvailable(False)

        url = reverse('homepage:mQuestView', args=(quest.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This quest is not available")

    # Test that if a quest should be available, it will be shown on the page
    def test_quest_available(self):
        # Make a quest with basic parameters
        quest = Quest.objects.create()
        quest.setName("Test Quest")
        quest.setAvailable(True)
        quest.save()
        url = reverse('homepage:mQuestView', args=(quest.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, quest.getName())


def create_QuestionView_Quest(question="N/A", choice="N/A"):
    quest = Quest.objects.create()

    question = quest.question_set.create()
    question.setQuestion(question)

    if (choice != "N/A"):
        choice = question.choice_set.create()
        choice.setChoice(choice)

    quest.save()
    return quest


class QuestionsViewTest(TestCase):

    def test_question_with_no_choices(self):
        # Test that a single question with no choices presents the proper page
        quest = create_QuestionView_Quest("Test Question")
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(quest.id, question.id))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This Question does not have any choices")

    def test_1_question(self):
        # Test that a single question produces its proper page
        quest = create_QuestionView_Quest("Test Question", "Test Choice")
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(quest.id, question.id))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.choice_set.get(pk=1).getChoice())

    def test_2_questions(self):
        quest = create_QuestionView_Quest("Test Question", "Test Choice")
        question = quest.question_set.get(pk=1)

        url = reverse('homepage:mQuest', args=(quest.id, question.id))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.choice_set.get(pk=1).getChoice())

        question2 = quest.question_set.create()
        question2.setQuestion("Test Question 2")

        choice2 = question2.choice_set.create()
        choice2.setChoice("Test Choice 2")

        url = reverse('homepage:mQuest', args=(quest.id, question2.id))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question2.choice_set.get(pk=2).getChoice())
