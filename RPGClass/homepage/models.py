from django.db import models


# Create your models here.
# Note for classes, any member prefaced by '_' will be private.
class Course(models.Model):
    # Public members
    def getName(self):
        return self._course_name

    def setName(self, name):
        self._course_name = name

    def getSection(self):
        return self._section_number

    def setSection(self, num):
        self._section_number = num

    # Private members
    _course_name = models.CharField(max_length=200)
    _section_number = models.IntegerField(default=0)


# Quest model: Defines the general information for a quest. This includes name, description, lives, etc.
# Quests can be create directly on the app, and can also be carried over from other software, and can also
# be individually created and updated for any avenues this app doesn't support.
class Quest(models.Model):
    # Public Members
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # Getters and setters
    def getName(self):
        return self._Quest_name

    def setName(self, name):
        self._Quest_name = name
        return "Name Changed successfully"

    def getDesc(self):
        return self._Quest_description

    def setDesc(self, desc):
        self._Quest_description = desc

    def getLives(self):
        return self._Num_lives

    def setLives(self, num):
        self._Num_lives = num
        return "Changed successfully"

    # Keeps track of the right answers for a quest
    def getXP(self):
        return self._Correct_answers

    def rightAnsChosen(self):
        self._Correct_answers += 1

    def setXP(self, numRight):
        self._Correct_answers = numRight

    # A quest should not be shown to the player if it is defined as such by the admin
    def getAvailable(self):
        return self._Is_available

    def setAvailable(self, available):
        self._Is_available = available
        return "Availability has been changed"

    # The quest type will determine how a quest will be handled by the app. The values are as follows:
    # 0: Quest type of zero means the app does nothing special. It takes the Quest name, XP gained, level progress,
    #    etc. Used when the quest is manually defined and updated by the admin.
    # 1: Quest type 1 is a standard quest, which would include multiple choice, short answer, essays, etc.

    # NOTE: Other types to be added in the future, such as imports from other software, file uploads, and anything
    # we may decided important
    def getType(self):
        return self._Quest_type

    def setType(self, questType):
        self._Quest_type = questType
        return "Type of quest updated"

    # Private members
    _Quest_name = models.CharField(max_length=200, default="N/A")
    _Quest_description = models.CharField(max_length=200, default="N/A")
    _Num_lives = models.IntegerField(default=0)
    _Correct_answers = models.IntegerField(default=0)
    _Is_available = models.BooleanField(default=False)
    _Quest_type = models.IntegerField(default=0)

    def __str__(self):
        msg = "This is Quest number:" + str(self.pk)
        return msg


# If an admin wishes, they may create quests directly in the app. This is opposed to it being on some other software,
# like BlackBoard
class Question(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)

    # Public members
    def getQuestion(self):
        return self._Question_text

    def setQuestion(self, text):
        self._Question_text = text
        return "Question changed"

    # Private members
    _Question_text = models.CharField(max_length=200, default="N/A")

    def __str__(self):
        msg = str(self.pk) + " " + str(self.getQuestion())
        return msg


class Choice(models.Model):
    # Public members
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def getChoice(self):
        return self._choice_text

    def setChoice(self, text):
        self._choice_text = text
        return "Changed successfully"

    def getCorrect(self):
        return self._isCorrectChoice

    def setCorrect(self, isAnswer):
        self._isCorrectChoice = isAnswer
        return "Correct answer chosen"

    # Private members
    _choice_text = models.CharField(max_length=200, default="N/A")
    _isCorrectChoice = models.BooleanField(default=False)

    def __str__(self):
        msg = str(self.pk) + ": Is " + str(self.getChoice()) + " the correct answer?  " + str(self.getCorrect())
        return msg
