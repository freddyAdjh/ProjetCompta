"""Gestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from StockCompta import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home,name="Home"),
    path('person/', views.saveperson,name="saveperson"),
    path('F/', views.createBill,name="createBill"),
    path('A/', views.addBillArticle,name="addBillArticle"),
    path('Edit/', views.EditBill,name="EditBill"),
    path('Sortie/', views.sortie,name="output"),
    path('Articles/', views.AllArticles,name="articles"),
    path('<int:id>/', views.getQty,name="getQty"),
    path('cession/', views.output,name="Sortie"),
    path('xls/', views.export_excel,name="export-excel"),
    path('outxls/', views.export_excel_out,name="export-excel-out"),
    
    path('update/', views.add_to_update,name="add_to_update"),
    path('AllOutput/', views.allOutput,name="allOutput"),
    path('Personnel/', views.allPeople,name="allPeople"),












    
    

]
