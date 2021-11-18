from django.db import models

# Create your models here.
# Note for classes, any member prefaced by '_' will be private.

# Quest model: Defines the general information for a quest. This includes name, description, lives, etc.
# Quests can be create directly on the app, and can also be carried over from other software, and can also
# be individually created and updated for any avenues this app doesn't support.
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


# Boss model: Defines the general information for a boss. This includes name, description, lives, etc.
# Bosses can be create directly on the app, and can also be carried over from other software, and can also
# be individually created and updated for any avenues this app doesn't support.
class Boss(models.Model):
    # Public Members

    # Getters and setters
    def getName(self):
        return self._Boss_name

    def setName(self, name):
        self._Boss_name = name
        return "Name Changed successfully"

    def getDesc(self):
        return self._Boss_description

    def setDesc(self, desc):
        self._Boss_description = desc

    def getLives(self):
        return self._Num_lives

    def setLives(self, num):
        self._Num_lives = num
        return "Changed successfully"

    # Keeps track of the right answers and XP for a boss
    def getXP(self):
        return self._Correct_answers

    def rightAnsChosen(self):
        self._Correct_answers += 2

    def setXP(self, numRight):
        self._Correct_answers = numRight

    # A boss should not be shown to the player if it is defined as such by the admin
    def getAvailable(self):
        return self._Is_available

    def setAvailable(self, available):
        self._Is_available = available
        return "Availability has been changed"

    # The boss type will determine how a boss will be handled by the app. The values are as follows:
    # 0: Boss type of zero means the app does nothing special. It takes the Boss name, XP gained, level progress,
    #    etc. Used when the boss is manually defined and updated by the admin.
    # 1: Boss type 1 is a standard quest, which would include multiple choice, short answer, essays, etc.

    # NOTE: Other types to be added in the future, such as imports from other software, projects, file uploads,
    # and anything we may decided important
    def getType(self):
        return self._Boss_type

    def setType(self, bossType):
        self._Boss_type = bossType
        return "Type of quest updated"


    # Private members of Boss
    _Boss_name = models.CharField(max_length=200, default="N/A")
    _Boss_description = models.CharField(max_length=200, default="N/A")
    _Num_lives = models.IntegerField(default=0)
    _Correct_answers = models.IntegerField(default=0)
    _Is_available = models.BooleanField(default=False)
    _Boss_type = models.IntegerField(default=0)

    def __str__(self):
        msg = "This is the Boss number:" + str(self.pk)
        return msg

# Rec model: Defines the name of the recommendation and if it is available
class Recs(models.Model):
    # Public Members

    # Getters and setters
    def getName(self):
        return self._Recs_name

    def setName(self, name):
        self._Recs_name = name
        return "Name Changed successfully"

    # A recommendation should not be shown to the player if it is defined as such by the admin
    def getAvailable(self):
        return self._Is_available

    def setAvailable(self, available):
        self._Is_available = available
        return "Availability has been changed"

    # Private members
    _Recs_name = models.CharField(max_length=200, default="N/A")
    _Is_available = models.BooleanField(default=False)

    def __str__(self):
        msg = "This is Recs number:" + str(self.pk)
        return msg

# If an admin wishes, they can add their own recommended topics
class Topic(models.Model):
    topic = models.ForeignKey(Recs, on_delete=models.CASCADE)

    # Public members
    def getTopic(self):
        return self._Topic_text

    def setTopic(self, text):
        self._Topic_text = text
        return "Question changed"

    # Private members
    _Topic_text = models.CharField(max_length=200, default="N/A")

    def __str__(self):
        msg = str(self.pk) + " " + str(self.getTopic())
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

# If an admin wishes, they may create bosses directly in the app. This is opposed to it being on some other software,
# like BlackBoard
class bossQuestion(models.Model):
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE)

    # Public members
    def getQuestion(self):
        return self._bossQuestion_text

    def setQuestion(self, text):
        self._bossQuestion_text = text
        return "Question changed"

    # Private members
    _bossQuestion_text = models.CharField(max_length=200, default="N/A")

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

class bossChoice(models.Model):
    # Public members
    bossQuestion = models.ForeignKey(bossQuestion, on_delete=models.CASCADE)

    def getChoice(self):
        return self._bossChoice_text

    def setChoice(self, text):
        self._bossChoice_text = text
        return "Changed successfully"

    def getCorrect(self):
        return self._isCorrectChoice

    def setCorrect(self, isAnswer):
        self._isCorrectChoice = isAnswer
        return "Correct answer chosen"

    # Private members
    _bossChoice_text = models.CharField(max_length=200, default="N/A")
    _isCorrectChoice = models.BooleanField(default=False)

    def __str__(self):
        msg = str(self.pk) + ": Is " + str(self.getChoice()) + " the correct answer?  " + str(self.getCorrect())
        return msg
