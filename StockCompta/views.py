from cProfile import label
from email.utils import parsedate_to_datetime
import json
from multiprocessing import context
from re import search, template
from turtle import towards
from unicodedata import category
from urllib import response
from django.shortcuts import render,HttpResponseRedirect,redirect
from .models import Article,Sortie,Bill,personnel,price_Class,Provider
from datetime import date,datetime
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth import authenticate,login,logout
from django.http import FileResponse,HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from django.contrib.auth.decorators import login_required

today=datetime.now().strftime('%Y-%m-%d')

def addItems(request):
    return render(request,'StockCompta/addPerson.html')

def saveperson(request):
    if request.method =="POST":
        email = request.POST['email']
        Name = request.POST['personName']
        contact = request.POST['contact']
        service = request.POST['service']

        rg = personnel(email = email,name = Name,numero = contact,service = service)
        rg.save()
    return redirect('addItems')

def saveArticle(request):
    if request.method =="POST":
        label = request.POST['label']
        price = request.POST['price']
        qte = request.POST['qte']
        seuil = request.POST['seuil']
        rq = price_Class(prix = price,date = today)
        rq.save()
        rg = Article(label=label,ActualQty=qte,limitQty=seuil,AddedDate=today,paramPrix=rq)
        rg.save()
    return redirect('addItems')




