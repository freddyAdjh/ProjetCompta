from cProfile import label
import email
from email.utils import parsedate_to_datetime
import json
import re
from unittest import result
from django.contrib.auth.models import User
from multiprocessing import context
from re import search, template
from turtle import towards
from unicodedata import category
from urllib import response
from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from .models import Article,Sortie,Bill,personnel,price_Class,Provider,Ligne_de_facture
from datetime import date,datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.http import FileResponse,HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from datetime import date
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


def Home(request):
    s = 0
    art = Article.objects.all()
    All = Ligne_de_facture.objects.all().values_list("ActualQty",'paramArticle','paramBill')
    art = art.count()
    pers = personnel.objects.all()
    pers = pers.count()
    for k in All:
        a = Article.objects.get(id=k[1])

        s +=a.paramPrix.prix*k[0]
    context = {
        "pers":pers,
        "art":art,
        "val":s
    }
    return render(request,'StockCompta/addPerson.html',context)

def saveperson(request):
    if request.method =="POST":
        email = request.POST['email']
        Name = request.POST['personName']
        contact = request.POST['contact']
        service = request.POST['service']
        if personnel.objects.filter(email = email,name = Name,numero = contact,service = service).exists():
            msg="Ce personnel est déjà répertorié"
            return render(request,'StockCompta/addPerson.html',{'msg1':msg})
        else:
            rg = personnel(email = email,name = Name,numero = contact,service = service)
            rg.save()
            Art = Article.objects.all()
            All = Ligne_de_facture.objects.all().values_list("ActualQty",'paramArticle','paramBill')

            art = Art.count()
            pers = personnel.objects.all()
            pers = pers.count()
            for k in All:
                a = Article.objects.get(id=k[1])

                s +=a.paramPrix.prix*k[0]
                context = {
                        "pers":pers,
                        "art":art,
                        "val":s
                    }

    return render(request,'StockCompta/addPerson.html',context)


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
        Bill_date = datetime.strptime(Bill_date,"%Y-%m-%d")
        P = price_Class(prix = Art_price,date = Bill_date)

        thisBill = Bill.objects.get(numero=Bill_number,date=Bill_date)
        Art = Article(label = Art_label,limitQty=Art_critik,paramPrix=P,AddedDate=Bill_date)
        if Article.objects.filter(label = Art_label,limitQty=Art_critik,AddedDate=Bill_date).exists():
            msg = "Cet article est déjà répertorié. Entrez en un autre"
            return render(request,'StockCompta/Bill.html',{"msg":msg})

        else:
            P.save()
            Art.save()
            L_F = Ligne_de_facture(paramArticle=Art,paramBill=thisBill,ActualQty = Art_qty)
            L_F.save()
            return render(request,'StockCompta/Bill.html',{'bill':thisBill})
    

    return redirect("addBillArticle")


def add_to_update(request):
    if request.method=="POST":
        Bill_number = request.POST.get('nf')
        Bill_date = request.POST.get('Bill')
        Art_label = request.POST.get('label') 
        Art_price = request.POST.get('price')
        Art_qty = request.POST.get('qte')
        Art_critik = request.POST.get('seuil')
        P = price_Class(prix = Art_price,date = Bill_date)

        thisBill = Bill.objects.get(numero=Bill_number,date=Bill_date)
        Art = Article(label = Art_label,limitQty=Art_critik,paramPrix=P,AddedDate=Bill_date)
        if Article.objects.filter(label = Art_label,limitQty=Art_critik,AddedDate=Bill_date).exists():
            msg = "Cet article est déjà répertorié. Entrez en un autre"
            return render(request,'StockCompta/Bill.html',{"msg":msg})

        else:
            P.save()
            Art.save()
            L_F = Ligne_de_facture(paramArticle=Art,paramBill=thisBill,ActualQty = Art_qty)
            L_F.save()
            return render(request,'StockCompta/updateBill.html',{'bill':thisBill})
    

    return redirect("add_to_update")

def EditBill(request):
    if request.method=="POST":
        numero = request.POST.get('BillNumber')
        provider = request.POST.get('Pro')
        code = request.POST.get('code')
        dateFacture = request.POST.get('BillDate')
        fournisseur = Provider.objects.get(label = provider,code=code)
        u = User.objects.get(username=request.user.username)
        bill = Bill.objects.get(numero=numero,date=dateFacture,paramFournisseur=fournisseur,paramUser=u)
        if Bill.objects.filter(numero=numero,date=dateFacture,paramFournisseur=fournisseur,paramUser=u).exists():
            context = {"bill":bill}
            return render(request,'StockCompta/updateBill.html',context)
    return render(request,'StockCompta/SearchBill.html')


def sortie(request):
    Art = Article.objects.order_by('label')
    Pers = personnel.objects.all()

    context = {"Articles":Art,"Personnel":Pers}
    return render(request,"StockCompta/Sortie.html",context)

def AllArticles(request):
    Art = Ligne_de_facture.objects.all()
    
    P = Paginator(Art,10)
    page_n = request.GET.get('page',1)
    try:
        Art = P.page(page_n)
    except EmptyPage:
        Art = P.page(1)

    return render(request,"StockCompta/Articles_pdf.html",{'Articles':Art})

def getQty(request,id):
    art = Article.objects.get(id=id)
    l = Ligne_de_facture.objects.get(paramArticle=art)
    details = {
         "article":l.paramArticle.paramPrix.prix,
        "facture":l.paramBill.numero,
        'qte':l.ActualQty
    }
    return JsonResponse(details)

def output(request):
    per = request.POST.get("author")
    product = int(request.POST.get("Article"))
    qty = int(request.POST.get("quantity"))

    art = Article.objects.get(id=product)

    l = Ligne_de_facture.objects.get(paramArticle=art)
    l.ActualQty -=qty
    per = personnel.objects.get(email=per)

    s = Sortie(paramArticle = art,paramPersonnel=per,qte=qty)
    s.save()
    l.save()
    msg = "Sortie d'article effectuée"
    context = {
        'msg':msg
    }

    return render(request,'StockCompta/Sortie.html',context)

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename = Articles{datetime.now()}.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Articles')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["Date d'ajout",'Numero de la facture','Désignation','quantité','Prix','Montant']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    allLines = Ligne_de_facture.objects.all().values_list("ActualQty",'paramArticle','paramBill')
    finalList = []
    for k in allLines:
        a = Article.objects.get(id=k[1])
        f = Bill.objects.get(id=k[2])
        m = k[0]*a.paramPrix.prix

        t = (a.AddedDate,f.numero,a.label,k[0],a.paramPrix.prix,m)

        finalList.append(t)
        t = ()


    

    for r in finalList:
        row_num+=1

        for col_num in range(len(r)):
            ws.write(row_num,col_num,str(r[col_num]),font_style)

    wb.save(response)

    return response


# def export_pdf(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = f'inline, attachment; filename = Articles{datetime.now()}.pdf'

#     response['Content-Transfer-Encoding'] = 'binary'

#     allLines = Ligne_de_facture.objects.all().values_list("ActualQty",'paramArticle','paramBill')
#     finalList = []
#     for k in allLines:
#         a = Article.objects.get(id=k[1])
#         f = Bill.objects.get(id=k[2])

#         t = (a.AddedDate,f.numero,a.label,k[0],a.paramPrix.prix)

#         finalList.append(t)
#         t = ()

#     html_string = render_to_string("StockCompta/articles_output.html",{'articles':finalList})
#     html = HTML(string=html_string)
#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()

#         output = open(output.name,'rb')
#         response.write(output.read())

#         return response



def allOutput(request):
    S = Sortie.objects.all()
    P = Paginator(S,10)
    page_n = request.GET.get('page',1)
    try:
        S = P.page(page_n)
    except EmptyPage:
        S = P.page(1)

    return render(request,"StockCompta/allOutput.html",{'out':S})

def allPeople(request):
    S = personnel.objects.all()
    P = Paginator(S,10)
    page_n = request.GET.get('page',1)
    try:
        S = P.page(page_n)
    except EmptyPage:
        S = P.page(1)

    return render(request,"StockCompta/personnel.html",{'Pers':S})

def export_excel_out(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename = Toutes les sorties {datetime.now()}.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sorties')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["Date de sortie",'beneficiaire','désignation','quantité','Prix','montant']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    allLines = Sortie.objects.all().values_list("Date",'paramPersonnel',"paramArticle",'qte')
    finalList = []
    for k in allLines:
        p = personnel.objects.get(email = k[1])
        a = Article.objects.get(id=k[2])


        t = (k[0],p.name,a.label,k[3],a.paramPrix.prix,k[3]*a.paramPrix.prix)

        finalList.append(t)
        t = ()


    

    for r in finalList:
        row_num+=1

        for col_num in range(len(r)):
            ws.write(row_num,col_num,str(r[col_num]),font_style)

    wb.save(response)

    return response