from django.contrib import admin

# Register your models here.

from .models import Article,Sortie,Bill,personnel,price_Class,Provider,Ligne_de_facture


@admin.register(Article)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','label','limitQty','AddedDate','paramPrix')

@admin.register(Sortie)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','Date','qte','paramArticle','paramPersonnel')


@admin.register(Bill)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','numero','date','paramFournisseur','paramUser')

@admin.register(Provider)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','label','code')


@admin.register(price_Class)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','prix','date')

@admin.register(personnel)

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','name','numero','service')

@admin.register(Ligne_de_facture)

class UserAdmin(admin.ModelAdmin):
    list_display = ('paramArticle','paramBill','ActualQty')
