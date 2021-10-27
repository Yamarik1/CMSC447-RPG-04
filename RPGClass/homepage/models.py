from django.db import models


# Create your models here.
# Note for classes, any member prefaced by '_' will be private.

# Quest model: Defines the general information for a quest. This includes name, description, lives, etc.
class Quest(models.Model):
    # Public Members

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
    def getRight(self):
        return self._Correct_answers

    def rightAnsChosen(self):
        self._Correct_answers += 1

    def setRight(self, numRight):
        self._Correct_answers = numRight

    # A quest should not be shown to the player if it is defined as such by the admin
    def getAvalible(self):
        return self._Is_available

    def setAvalible(self, available):
        _Is_avalible = available
        return "Availability has been changed"

    # Protected members

    # Private members
    _Quest_name = models.CharField(max_length=200, default="N/A")
    _Quest_description = models.CharField(max_length=200, default="N/A")
    _Num_lives = models.IntegerField(default=0)
    _Correct_answers = models.IntegerField(default=0)
    _Is_available = models.BooleanField(default=False)

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
