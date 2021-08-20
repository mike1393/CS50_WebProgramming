from django.shortcuts import render
import datetime

# Create your views here.

def index(request):
    return render(request, "newyear/index.html",{
        "result":CheckNewYear()
    })

def CheckNewYear():
    now = datetime.datetime.now()
    return now.month == 1 and now.day == 1