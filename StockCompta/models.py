from email.policy import default
from pickle import TRUE
from pyexpat import model
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

# class personnel

class personnel(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50,default=None)
    numero = models.IntegerField()
    service = models.CharField(max_length=50,default=None)

# class prix
class price_Class(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    prix = models.IntegerField()
    date = models.DateField()

# class fournisseur
class Provider(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    label = models.CharField(max_length=25)
    code = models.CharField(max_length=30)


# class Facture
class Bill(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    numero = models.IntegerField()
    date = models.DateField()
    paramFournisseur = models.ForeignKey(Provider,null=True,on_delete=models.CASCADE)
    paramUser = models.ForeignKey(User,null=True,on_delete=models.CASCADE)


# class article

class Article(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    label = models.CharField(max_length=30)
    ActualQty = models.IntegerField()
    limitQty = models.IntegerField()
    AddedDate = models.DateField()
    paramPrix = models.ForeignKey(price_Class,null=True,on_delete=models.CASCADE)

    
# class d'association sortie

class Sortie(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    Date = models.DateField()
    qte = models.IntegerField()
    paramArticle = models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    paramPersonnel = models.ForeignKey(personnel,null=True,on_delete=models.CASCADE)

