Steps for running current iteration of the project:

1. Start a Python Project with the name 'CMSC447-RPG-04'

2. Download the current release of the project, and copy the files into the Python project started

3. change directory to the django project, using 'cd PRGClass' in terminal

4. Install the requirements file
    'pip install -r requirements.txt'

5. Add a file named '.env' to the 'RPGClass' folder (the same folder as manage.py)

6. In the .env file, add a line 'SECRET_KEY=' and then add anything after the '=' (Without quotation marks)
    Note: This is done to keep the Secret key used in the development secret, so we don't commit it to GitHub

7. initialize the database with 'python manage.py makemigrations homepage' and then 'python manage.py migrate' in terminal

8. run the command 'python manage.py runserver' in terminal, and go to the local server

9. add '/homepage/' to the end of the url


To allow for proper navigation of the site:

1: You will be brought to a page that will allow you to login, or create an account.

2: Create an account in order to view the site

3: When on the site, hit the 'Initialize' button on the homepage, which will set up the database to some test values used

4: From there, you can see the features implemented, which for this iteration, are the main quests, account creation,
   and the skeleton for the profile page.


For Testing:

Run the command 'py manage.py test homepage.tests' and 'py manage.py test accounts.tests' to run the tests.

to run the selenium test in accounts, run command 'py manage.py test homepage.tests_selenium'
***created separate test because selenium takes a long time

before running tests in homepage:


1:update the geck_path in tests.py file in homepage to your local path of the geckodriver.exe

2:make sure you have firefox downloaded, haven't tried it on other browsers yet



