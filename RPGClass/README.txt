Steps for running current iteration of the project:
1. Start a Python Project with the name 'CMSC447-RPG-04'

2. Download the current release of the project, and cop the files into the Python project started

3. Install the requirements file
    'pip install -r requirements.txt'

4. initialize the database with 'python manage.py makemigrations' and then 'python manage.py migrate' in terminal

5. run the command 'python manage.py runserver' in terminal, and go to the local server

6. add '/homepage/' to the end of the url

To allow for proper navigation of the site:

1: After the homepage has been reached, a button with 'initialize', should appear; click that button.
    Note: This initializes the database to test values, which is easier than needing to go into the shell each time

2: From there, you can navigate the parts of the page that are currently available.

