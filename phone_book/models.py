from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def can_delete(self):
        return not self.email_set.exists() \
               and not self.phone_set.exists()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Phone(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.phone


class Email(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    email = models.EmailField()

    def __str__(self):
        return self.email
