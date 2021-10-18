Steps for running current iteration of the project:
1. the requirements.txt file must be installed on the machine, which can be done with a virtual enviornment
2. A Django project should be started named PRGCLass
3. The current Release can be copied to the project, and all old files can be overwritten
4. In the Settings.py file, add the following statement to INSTALLED_APPS
    'homepage.apps.HomepageConfig',
    to the list.
5. Use 'py manage.py runserver' in terminal, and then add 'homepage/' to the url
6. To run tests, use 'python manage.py test' to see the tests run

