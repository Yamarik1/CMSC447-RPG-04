from django.db import models


class Course_General(models.Model):
    # Public members
    def getName(self):
        return self._course_name

    def setName(self, name):
        self._course_name = name

    def getSection(self):
        return self._section_number

    def setSection(self, num):
        self._section_number = num

    def getCourseID(self):
        return self._course_id

    def setCourseID(self, ID):
        self._course_id = ID

    def hashKey(self, size, keyVal):
        a = 21
        b = 15
        p = 6151

        key = (((keyVal * a) + b) % p) % size
        return key

    # Private members
    _course_name = models.CharField(max_length=200)
    _section_number = models.IntegerField(default=0)
    # course_id is a unique 6 digit number used to identify a course
    _course_id = models.IntegerField(default=0)


class Student_courseList(models.Model):
    course_general = models.ManyToManyField(Course_General)
    student = models.OneToOneField('accounts.Student', on_delete=models.CASCADE, blank=True, null=True)

    def getName(self):
        return self._student_name

    def setName(self, name):
        self._student_name = name

    def setXP(self, xp):
        self._curr_XP = xp

    def updateXP(self, xp):
        self._curr_XP = self._curr_XP + xp

    def getXP(self):
        return self._curr_XP

    def addXP(self, xp):
        self._curr_XP += xp

    def setCoins(self, coins):
        self._coins = coins

    def getCoins(self):
        return self._coins

    _student_name = models.CharField(max_length=200)
    _curr_XP = models.IntegerField(default=0)
    _coins = models.IntegerField(default=0)


# Create your models here.
# Note for classes, any member prefaced by '_' will be private.
#from RPGClass.accounts.models import Student
from django.apps import apps

class Course(models.Model):

    specific_student = models.ForeignKey(Student_courseList, on_delete=models.CASCADE)
    # Public members
    def getName(self):
        return self._course_name

    def setName(self, name):
        self._course_name = name

    def getSection(self):
        return self._section_number

    def setSection(self, num):
        self._section_number = num

    def getCourseID(self):
        return self._course_id

    def setCourseID(self, ID):
        self._course_id = ID

    # Xp and levels for the current course, which will be separated by course
    def getTotalXP(self):
        return self._total_XP

    def setTotalXP(self, xp):
        self._total_XP = xp
        return "Total XP updated"

    def getCurrXP(self):
        return self._curr_XP

    # When a quest is completed, update the XP gained in the course
    def updateXP(self, gainedXP):
        self._curr_XP += gainedXP
        tempXP = self.getCurrXP()
        self._total_XP += gainedXP
        # For every multiple of _max_xp that tempXP is greater than, the level should be increased by 1
        while tempXP >= self.getMaxXP():
            tempXP = tempXP - self.getMaxXP()
            self._course_level += 1

        self._curr_XP = tempXP

    def setCurrXP(self, xp):
        self._course_XP = xp
        return "XP updated"

    def getNextLevel(self):
        return self.getMaxXP() - self.getCurrXP()

    def getMaxXP(self):
        return self._max_XP

    def setMaxXP(self, xp):
        self._max_XP = xp
        return "Max XP updated"

    def getCourseLevel(self):
        return self._course_level

    def setCourseLevel(self, level):
        self._course_level = level
        return "Level updated"

    # This function will take the course_id, and will then Hash it to find where it will be in CourseGeneral
    def hashKey(self, size, keyVal):
        a = 21
        b = 15
        p = 6151

        key = (((keyVal * a) + b) % p) % size
        return key

    # Private members
    _course_name = models.CharField(max_length=200)
    _section_number = models.IntegerField(default=0)
    _course_id = models.IntegerField(default=0)

    # course_XP and total_XP are two separate values. Total XP is all the Xp gained in the course
    # and course XP is the value of _max_XP - XP needed to get to the next level
    _curr_XP = models.IntegerField(default=0)
    _total_XP = models.IntegerField(default=0)

    _course_level = models.IntegerField(default=1)

    # _max_XP  is the xP needed to gain a level
    _max_XP = models.IntegerField(default=0)

class Student_course(models.Model):

    def setXP(self, xp):
        self._curr_XP = xp

    def getXP(self):
        return self._curr_XP

    def addXP(self, xp):
        self._curr_XP += xp

    def setCoins(self, coins):
        self._coins = coins

    def getCoins(self):
        return self._coins

    def getLevel(self):
        return self._level

    def addLevel(self, level):
        self._level += level

    def getCourseName(self):
         return self._course_name

    def setCourseName(self, name):
        self._course_name = name

    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    _curr_XP = models.IntegerField(default=0)
    _coins = models.IntegerField(default=0)
    _course_id = models.IntegerField(default=0)
    _course_name = models.CharField(max_length=200, default="N/A")
    _level = models.IntegerField(default=1)
    skills = {}


# Quest model: Defines the general information for a quest. This includes name, description, lives, etc.
# Quests can be create directly on the app, and can also be carried over from other software, and can also
# be individually created and updated for any avenues this app doesn't support.
class Quest(models.Model):
    # Public Members
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student_course, on_delete=models.CASCADE, blank=True, null=True)

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

    def subHeart(self):
        self._Num_lives -= 1

    # Keeps track of the right answers for a quest
    def getXP(self):
        return self._Correct_answers

    def getCorr(self):
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

    def getCompleted(self):
        return self._Is_completed

    def setCompleted(self, complete):
        self._Is_completed = complete
        return "Completion has been changed"

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
    _Is_completed = models.BooleanField(default=False)
    _Quest_type = models.IntegerField(default=0)

    def __str__(self):
        msg = "This is Quest number:" + str(self.pk)
        return msg


# Side quest model has the same logic as the main quest model. We wanted to add it as a separate table in the database
# So we can differentiate between the two. The idea is that while the logic of their implementation may be the same,
# the actual content added to them will be different, so we wanted to give the admin the ability to more easily
# differentiate between them.
class SideQuest(models.Model):
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

    def subHeart(self):
        self._Num_lives -= 1

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

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

    def subHeart(self):
        self._Num_lives -= 1

    def setLives(self, num):
        self._Num_lives = num
        return "Changed successfully"

    # Keeps track of the right answers and XP for a boss
    def getXP(self):
        return self._Correct_answers

    def rightAnsChosen(self):
        self._Correct_answers += 1

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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

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
    # A question can belong to either a main quest of a side quest, so there are two possible ForeignKeys in this model
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, blank=True, null=True)
    sidequest = models.ForeignKey(SideQuest, on_delete=models.CASCADE, blank=True, null=True)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE, blank=True, null=True)

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
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

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


class Skill(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
        return "Changed successfully"

    def getDesc(self):
        return self._description

    def setDesc(self, desc):
        self._description = desc
        return True

    def getCost(self):
        return self._cost

    def setCost(self, cost):
        self._cost = cost
        return True

    def getId(self):
        return self._id

    def setId(self, id):
        self._id = id
        return "Changed successfully"

    _name = models.CharField(max_length=200, default="N/A")
    _description = models.CharField(max_length=200, default="N/A")
    _cost = models.IntegerField(default=0)
    _id = models.CharField(max_length=200, default="N/A")


