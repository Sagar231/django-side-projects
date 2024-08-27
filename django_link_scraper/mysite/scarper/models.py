from django.db import models
import collections

# Create your models here.

class Link(models.Model):

    def __str__(self):
        return str(self.name)
    
    address = models.CharField(max_length=1000,null=True,blank=True)
    name = models.CharField(max_length=1000,null=True,blank=True)
