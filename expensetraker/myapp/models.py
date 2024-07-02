from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name