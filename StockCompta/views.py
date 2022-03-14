from cProfile import label
from email.utils import parsedate_to_datetime
import json
from re import search
from unicodedata import category
from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import PutArticle,Output
from .models import Article,Sortie
from datetime import datetime,date
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth import authenticate,login,logout
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def add_show(request):
    if request.method =="POST":
        fm = PutArticle(request.POST)
        if fm.is_valid():
            lb = fm.cleaned_data['label']
            p = fm.cleaned_data['price']
            aq = fm.cleaned_data['ActualQty']
            lq = fm.cleaned_data['limitQty']
            rg = Article(label=lb,price=p,ActualQty=aq,limitQty=lq)
            rg.save()
            return redirect("addandshow")
    else:
        fm = PutArticle()
    std = Article.objects.all()
    num = len(std)
    rup=0
    for s in std:
        if s.ActualQty - s.limitQty <=5:
            rup+=1
    p = Paginator(std,5)
    page_num = request.GET.get("page",1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    
    return render(request,'StockCompta/addandshow.html',{'form':fm,'art':page,"r":rup,'num':num})

def listR(request):
    std = Article.objects.all()
    rup=0
    trup = []
    for s in std:
        if s.ActualQty - s.limitQty <=5:
            trup.append(s)
    return redirect("list",{"q":trup})

def conf(request,id):
    p = Article.objects.get(pk=id)
    return render(request,"StockCompta/addandshow.html",{"item":p})

def invent(request):
    all = Sortie.objects.all()
    S = set()
    for i in all:
        S.add(i.beneficiary)
    if request.method =="POST":
        fm = Output(request.POST)
        
        if fm.is_valid():
            b = fm.cleaned_data['beneficiary']
            lb = fm.cleaned_data['label']
            qte = fm.cleaned_data['qte']
            serv = fm.cleaned_data['service']
            act = Article.objects.get(label=lb)
            if act.ActualQty >qte:
                rg = Sortie(beneficiary=b,label=lb,qte=qte,service=serv)
                obj = Article.objects.get(label=lb)
                obj.ActualQty = act.ActualQty-qte
                obj.save()
                rg.save()
                return redirect("invent")
            else:
                msg = "Stock de "+lb+" insuffisant "
                return render(request,'StockCompta/home.html',{'form':fm,'msg':msg,'S':S})
                
    else:
        fm = Output()
    return render(request,'StockCompta/home.html',{'form':fm,'S':S})

    
def login_user(request):
    if request.method =="POST":
        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("addandshow")
        else:
            return redirect("login")

    else:

        return render(request,"StockCompta/index.html")
        

def out(request):
    logout(request)
    return redirect("login")

def recap_pdf(request):
    buf = io.BytesIO()

    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",13)

    S = Article.objects.all()

    lines = []

    for v in S:
        lines.append(v.label)
        lines.append(v.price)
        lines.append(v.ActualQty)
        lines.append(v.limitQty)
        lines.append("================================================")
    
    for line in lines:
        line = str(line)
        textob.textLine(line)
    


    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    n = str(date.today())
    return FileResponse(buf,as_attachment=True,filename='inventaire '+n+'.pdf')

def get(request,id):
    pi = Article.objects.get(pk=id)

    return render(request ,'StockCompta/addandshow.html',{"q":pi})

def supp(request,id):
    if request.method=="POST":
        pi = Article.objects.get(pk=id)
        pi.delete()
    return HttpResponseRedirect("/a")


def search(request):
    if "search" in request.POST:
        search = request.POST['search']
        posts = Sortie.objects.filter(beneficiary__icontains = search)
    
    else:
        posts = Sortie.objects.all()
    
    c = posts.count()
    if c >1:
        msg = f'{c} resultats sur'
    else:
        msg = f'{c} resultat'
    paginator = Paginator(posts,15)
    page_num = request.GET.get("page",1)
    try:
        posts_obj = paginator.page(page_num)
    except EmptyPage:
        posts_obj = paginator.page(1)
    return render(request,'StockCompta/list.html',{'res':posts_obj,'msg':msg,'s':search})

def downloadby(request,s):
    buf = io.BytesIO()

    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)

    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",13)

    S = Sortie.objects.filter(beneficiary__icontains = s)

    lines = []
    
    lines.append(s)
    
    lines.append("______________________________________________________________")
    for v in S:
        t = []
        t.append(v.jour)
        t.append(v.mois)
        t.append(v.an)

        lines.append("/".join(t))
        lines.append(v.label)
        lines.append(v.qte)
        lines.append(v.service)

        lines.append("================================================")
    
    for line in lines:
        line = str(line)
        textob.textLine(line)
    


    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    n = str(date.today())
    return FileResponse(buf,as_attachment=True,filename=s+'-'+n+'.pdf')

def get(request,id):
    pi = Article.objects.get(pk=id)

    return render(request ,'StockCompta/addandshow.html',{"q":pi})


        