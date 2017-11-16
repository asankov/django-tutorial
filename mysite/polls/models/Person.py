from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        print("Saving {}".format(str(self)))
        super(Person, self).save(*args, **kwargs)