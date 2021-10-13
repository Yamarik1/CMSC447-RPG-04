from django.db import models


# Create your models here.

class Option(models.Model):

    Option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.Option_text
