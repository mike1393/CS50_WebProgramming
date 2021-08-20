from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def page(request, name):
    return render(request, "hello/page.html",{
        "name":name.capitalize()
    })