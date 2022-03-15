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
    path('a/', views.add_show,name="addandshow"),
    # path('', views.login_user,name="login_user"),
    path('conf/<int:id>', views.conf,name="conf"),
    path('Sorties/', views.AllOut,name="AllOut"),
    path('Gen-Pdf/', views.render_pdf,name="render_pdf"),




    path('',views.login_user,name="login"),
    path('list/', views.listR,name="list"),
    path('del/<int:id>/', views.supp,name="suppdel"),
    path('<int:id>', views.get,name="get"),




    
    path('', views.out,name="out"),
    path('down/<str:s>/', views.downloadby,name="downloadby"),
     path('search', views.search,name="search"),

    path('r/', views.invent,name="invent"),
    path('recap_pdf/', views.recap_pdf,name="recap_pdf"),
    path('articles/', views.Articles,name="Articles"),

    path('edit/<int:id>', views.Edit,name="Edit"),
    path('update/', views.update,name="update"),

]
