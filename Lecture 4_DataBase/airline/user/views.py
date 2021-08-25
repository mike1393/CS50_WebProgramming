from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/user.html")        

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user/login.html",{
                "message": "Wrong username or Password"
            })
    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    return render(request, "user/login.html", {
        "message": "Logged Out"
    })