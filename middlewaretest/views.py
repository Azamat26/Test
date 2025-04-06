from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Ok1")

def contact(request):
    return HttpResponse("ok2")
