from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth import get_user_model, login
from selenium.webdriver.common.by import By
from selenium import webdriver

from .models import Course, Quest, Question, Choice

geck_path: str ='/Users/matt/PycharmProjects/CMSC447-RPG-04/RPGClass/homepage/Gecko/geckodriver.exe'

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
