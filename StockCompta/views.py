from cProfile import label
from email.utils import parsedate_to_datetime
import json
from django.contrib.auth.models import User
from multiprocessing import context
from re import search, template
from turtle import towards
from unicodedata import category
from urllib import response
from django.shortcuts import render,HttpResponseRedirect,redirect
from .models import Article,Sortie,Bill,personnel,price_Class,Provider,Ligne_de_facture
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


def createBill(request):
    if request.method=="POST":
        numero = request.POST.get('BillNumber')
        provider = request.POST.get('Pro')
        code = request.POST.get('code')
        dateFacture = request.POST.get('BillDate')
    
        if Bill.objects.filter(numero=numero,date=dateFacture).exists():
            msg = "Facture existante"
            return render(request,'StockCompta/addPerson.html',{'msg':msg})

        else:
            fournisseur = Provider(label = provider,code=code)
            if fournisseur not in Provider.objects.all():
                fournisseur.save()
                u = User.objects.get(username=request.user.username)
                bill = Bill(numero=numero,date=dateFacture,paramFournisseur=fournisseur,paramUser=u)
                bill.save()
                context = {"bill":bill}
                return render(request,'StockCompta/Bill.html',context)



    return render(request,'StockCompta/addPerson.html')


def addBillArticle(request):
    if request.method=="POST":
        Bill_number = request.POST.get('nf')
        Bill_date = request.POST.get('Bill')
        Art_label = request.POST.get('label') 
        Art_price = request.POST.get('price')
        Art_qty = request.POST.get('qte')
        Art_critik = request.POST.get('seuil')

        P = price_Class(prix = Art_price,date = Bill_date)
        P.save()

        if Article.objects.filter(paramPrix=P,AddedDate=Bill_date).exists():
            msg = "Cet article est déjà référencé dans le stock"
            return render(request,'',{"msg":msg})
        else:
            thisBill = Bill.objects.get(numero=Bill_number,date=Bill_date)
            Art = Article(label = Art_label,limitQty=Art_critik,paramPrix=P,AddedDate=Bill_date)
            Art.save()
            L_F = Ligne_de_facture(paramArticle=Art,paramBill=thisBill,ActualQty = Art_qty)
            L_F.save()
            return render(request,'StockCompta/Bill.html',{'bill':thisBill})


    return redirect("addBillArticle")






