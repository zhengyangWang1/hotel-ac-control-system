from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from manager import models
import datetime


# Create your views here.

def login(request):
    return render(request, 'manager_login.html')
