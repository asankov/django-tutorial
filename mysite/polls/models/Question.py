import datetime

from django.db import models
from django.utils import timezone

from .person import Person

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    people = models.ForeignKey(Person, on_delete=models.CASCADE)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):
        print("Saving {}".format(str(self)))
        super(Question, self).save(*args, **kwargs)