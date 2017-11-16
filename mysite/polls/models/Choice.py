from django.db import models

from .Question import Question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        print("Saving {}".format(str(self)))
        super(Choice, self).save(*args, **kwargs)