from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)   # TODO: do not save password 


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)
    def __str__(self):
        return f"{self.user} - token"


class Expense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.amount} - {self.date}"


class Income(models.Model):
    title = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.amount} - {self.date}"
    