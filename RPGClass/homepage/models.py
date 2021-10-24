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

    def setLives(self):
        return self._Num_lives

    # Protected members

    # Private members
    _Quest_name = models.CharField(max_length=200, default="N/A")
    _Quest_description = models.CharField(max_length=200, default="N/A")
    _Num_lives = models.IntegerField(default=0)

    def __str__(self):
        msg = "This is Quest number:" + str(self.pk)
        return msg
