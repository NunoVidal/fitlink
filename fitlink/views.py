from django.shortcuts import render
from .models import Planos
# Create your views here.

def index(request):
    return render(request,'index.html',{})