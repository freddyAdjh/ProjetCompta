from django.contrib import admin

# Register your models here.

from .models import Article,Sortie

@admin.register(Article)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','label','price','ActualQty','limitQty')

@admin.register(Sortie)

class UserAdmin(admin.ModelAdmin):
    list_display = ('jour','mois','an','beneficiary','label','qte','service')
