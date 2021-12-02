from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Student(models.Model):

    def getStudentName(self):
        return self._student_name

    def setStudentName(self, name):
        self._student_name = name
        return True

    def getNickname(self):
        return self._Nickname

    def setNickname(self, name):
        self._Nickname = name
        return True

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _student_name = models.CharField(max_length=200, default="John Doe")
    _Nickname = models.CharField(max_length=200, default="John Doe")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.student.save()