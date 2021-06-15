from django.db import models
from administration.models import User
from django.urls import reverse


# Create your models here.
class Parent(models.Model):
    name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=300)
    contact = models.IntegerField()
    email = models.EmailField(max_length=50)
    district = models.CharField(max_length=40)
    address = models.CharField(max_length=200)


    class Meta:
        ordering = ('name',)

    

    def __str__(self):
        return self.name


    def get_absolute_url(self): # new
        return reverse('allparent')

