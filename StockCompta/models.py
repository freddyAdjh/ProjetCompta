from email.policy import default
from pickle import TRUE
from pyexpat import model
from django.db import models
from datetime import datetime
# Create your models here.
class Article(models.Model):
    label = models.CharField(max_length=30)
    price =  models.IntegerField()
    ActualQty = models.IntegerField()
    limitQty = models.IntegerField()

class Sortie(models.Model):
    jour = models.CharField(max_length=15,default=datetime.now().day)
    mois = models.CharField(max_length=15,default=datetime.now().month)
    an = models.CharField(max_length=15,default=datetime.now().year)
    beneficiary = models.CharField(max_length=50,null=True)
    label = models.CharField(max_length=50,null=True)
    qte = models.IntegerField()
    service = models.CharField(max_length=50,null=True)


    