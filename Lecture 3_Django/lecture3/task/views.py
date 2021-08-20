from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class NewTaskForm(forms.Form):
    """NewTaskForm definition."""
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"]=[]
    return render(request, "task/index.html",{
        "tasks":request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("task:index"))
        else:
            render(request, "task/add.html",{
                "form": form
            })
    return render(request, "task/add.html", {
        "form": NewTaskForm()
    })