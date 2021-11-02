from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.urls import reverse
from selenium import webdriver

# Create your tests here.
#tests logging in
class LoginTest(TestCase):
    #creates test user to login with
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    #deletes user
    def tearDown(self):
        self.user.delete()

    #test if you can access this
    def test_signup_page_url(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')

    #test if you can access by name
    def test_signup_view_name(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')

    #test if login with right credentials work
    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    #test with wrong credentials for both
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

#test the logout function
class LogoutTest(TestCase):
    #create users
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    #delete users
    def tearDown(self):
        self.user.delete()

    #Note: you should never use get with logout because it should only be used for positng, so we test this feature by posting
    #plus, we can only try to find it since we have no users logged in, which is why it's 302 and not 200.

    #test if you can access this
    def test_logout_page_url(self):
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    #test if you can access by name
    def test_logout_view_name(self):
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    #tests the logout function.
    #the button on the homescreen just goes to 'accounts/logout/' and logs out the user
    def test_logout(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get('/homepage/')
        self.assertEquals(response.status_code, 200)

        c = self.client.post('/accounts/logout/')

        response = self.client.get('/homepage/')
        self.assertEquals(response.status_code, 302)

#test signing up users
class SignupTests(TestCase):

    #doesnt create users yet but will use these credentials
    def setUp(self):
        self.username = 'test2'
        self.password = '11test11'

    #test if you can access this
    def test_signup_page_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/signup.html')

    #test if you can access by name
    def test_signup_view_name(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/signup.html')

    #test if you can sign up with certain credentials
    def test_signup_form(self):
        #sign up form has 3 entries: username, passwors and password comfirmation
        response = self.client.post(reverse('accounts:signup'), data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        #should on be found since signing up redirects you to home screen
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        #user chould be created
        self.assertEqual(users.count(), 1)

    def test_signup_form_bad(self):
        response = self.client.post(reverse('accounts:signup'), data={
            'username': self.username,
            'password1': 'test',
            'password2': 'test1'
        })
        #should go back to signup with wrong crednetials
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('accounts:signup'), data={
            'username': self.username,
            'password1': 'test',
            'password2': 'test'
        })
        #same thing above
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        #should be no users created
        self.assertEqual(users.count(), 0)