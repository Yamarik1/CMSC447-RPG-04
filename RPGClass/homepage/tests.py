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


class MainQuest(TestCase):

    # Test that correct answers can be found by the models
    def test_correct_1(self, quest=None):
        # Create a test Quest
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
                    answerArray[i-1] = True
                counter += 1
        # Test fails if there is any false in the list, thus no correct answer is chosen
        self.assertIs(False in answerArray, False)

