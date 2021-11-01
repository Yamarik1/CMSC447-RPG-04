Steps for running current iteration of the project:
1. the requirements.txt file must be installed on the machine, which can be done with a virtual environment.
    NOTE: For the current interation, you can also just install django, those are the only dependencies for now.
2. A Django project should be started named RPGCLass.
3. The current Release can be copied to the python (not django) project, and all old files can be overwritten
4. In the Settings.py file, add the following statement to INSTALLED_APPS
    'homepage.apps.HomepageConfig',
    to the list.
5. Change directory to 'RPGClass' in terminal.
6. Use 'py manage.py runserver' in terminal, and then add '/homepage/' to the url.
7. To run tests, use 'python manage.py test homepage' to see the tests run.

things to add to project(login):
    settings:
        in templates in 'DIRS' array:- str(BASE_DIR.joinpath('login'))
        add LOGIN_REDIRECT_URL = 'homepage/' at the very bottom of settings
        add LOGOUT_REDIRECT_URL = '/' at the bottom of settings

    urls.py:
        in urlpatterns - path('accounts/', include('django.contrib.auth.urls'))

    to run test:
        1)

