from cProfile import label
from dataclasses import fields
from django.core import validators
from django import forms


from .models import Article,Sortie



class PutArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'label',
            'price',
            'ActualQty',
            'limitQty'
        ]
        widgets={
            'label':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'ActualQty':forms.NumberInput(attrs={'class':'form-control'}),
            'limitQty':forms.NumberInput(attrs={'class':'form-control'}),
        }

class Output(forms.ModelForm):
    class Meta:
        model = Sortie
        fields = ['jour','mois','an','beneficiary','label','qte','service']

        widgets={
            'jour':forms.HiddenInput(),
            'mois':forms.HiddenInput(),
            'an':forms.HiddenInput(),
            'beneficiary':forms.TextInput(attrs={'class':'form-control'}),
            'label':forms.TextInput(attrs={'class':'form-control'}),
            'qte':forms.NumberInput(attrs={'class':'form-control'}),
            'service':forms.TextInput(attrs={'class':'form-control'}),
        }

