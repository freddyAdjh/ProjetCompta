from cProfile import label
from email.utils import parsedate_to_datetime
import json
from multiprocessing import context
from re import search, template
from unicodedata import category
from urllib import response
from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import PutArticle,Output
from .models import Article,Sortie
from datetime import datetime,date
from django.utils import timezone
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

    S = Article.objects.all()
    template_path = 'StockCompta/pdfReport3.html'
    n = datetime.today()
    context = {'Articles':S}
    response = HttpResponse(content_type = 'application/pdf')
    response['content-Disposition'] = f'filename="Articles.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html,dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur')
    return response

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
        msg = f'{c} resultats'
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

    S = Sortie.objects.filter(beneficiary__icontains = s)
    template_path = 'StockCompta/pdfReport2.html'
    n = datetime.today()
    context = {'Sorties':S,'s':s}
    response = HttpResponse(content_type = 'application/pdf')
    response['content-Disposition'] = f'filename="{s} - {n}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html,dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur')
    return response


def get(request,id):
    pi = Article.objects.get(pk=id)

    return render(request ,'StockCompta/addandshow.html',{"q":pi})

def AllOut(request):
    posts = Sortie.objects.all()
    
    c = posts.count()
    if c >1:
        msg = f'{c} resultats'
    else:
        msg = f'{c} resultat'
    paginator = Paginator(posts,15)
    page_num = request.GET.get("page",1)
    try:
        posts_obj = paginator.page(page_num)
    except EmptyPage:
        posts_obj = paginator.page(1)
    return render(request,'StockCompta/allout.html',{'res':posts_obj,'msg':msg})


def render_pdf(request):
    posts = Sortie.objects.all()

    template_path = 'StockCompta/pdfReport.html'
    context = {'Sorties':posts,'D':datetime.today()}
    response = HttpResponse(content_type = 'application/pdf')
    response['content-Disposition'] = 'filename="Sorties.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html,dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur')
    return response

def Articles(request):
    A = Article.objects.all()
    c = A.count()
    if c >1:
        msg = f'{c} Articles'
    else:
        msg = f'{c} Article'
    paginator = Paginator(A,15)
    page_num = request.GET.get("page",1)
    try:
        posts_obj = paginator.page(page_num)
    except EmptyPage:
        posts_obj = paginator.page(1)
    return render(request,'StockCompta/Articles.html',{'Articles':posts_obj,'msg':msg})

def Edit(request,id):
    p = Article.objects.get(pk=id)
    context = {'p':p}
    return render(request,'StockCompta/edit.html',context)

def update(request):
    lb = request.POST['label']
    p = request.POST['price']
    aq = request.POST['ActualQty']
    lq = request.POST['limitQty']
    obj = Article.objects.get(label=lb)
    obj.label=lb
    obj.price=p
    obj.ActualQty=aq
    obj.limitQty=lq
    obj.save()
    return redirect("Articles")