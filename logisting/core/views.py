from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Това е началната страница.")

def about(request):
    return HttpResponse("Това е страницата за нас.")

def contact(request):
    return HttpResponse("Това е страницата за контакт.")
