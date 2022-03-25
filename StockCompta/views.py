from cProfile import label
from email.utils import parsedate_to_datetime
import json
from multiprocessing import context
from re import search, template
from unicodedata import category
from urllib import response
from django.shortcuts import render,HttpResponseRedirect,redirect
from .models import Article,Sortie,Bill,personnel,price_Class,Provider
from datetime import datetime
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


