from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return HttpResponseRedirect(reverse("wiki_index"))

def wiki_index(request):
    print("=============HOME================")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search_index(request):
    print("=============Search================")
    try:
        search_term = request.GET["q"]
        message=""
        result, file_list = util.search_entries(search_term)
        print(f"{result},{file_list}")
        if result == 0:
            return HttpResponseRedirect(reverse("entry", args=(file_list[0],)))
        elif result == 1:
            if len(file_list) > 0:
                message=f"Page \" {search_term} \" was not found, but we gathered similar results for you. "
                return render(request, "encyclopedia/search.html", {
                "message": message,
                "entries": file_list,
                "search_term":search_term
            })
            else:
                message=f"Page \" {search_term} \" or other similar results cannot be found. "
                return render(request, "encyclopedia/search.html", {
                "message": message,
                "entries": file_list,
                "search_term":search_term
            })
    except KeyError:
        return HttpResponseRedirect(reverse("wiki_index"))
        
    
def entry(request,title):
    print("=============Entry================")

    return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content": util.show_entry(title)
    })

def edit(request,title):
    content = util.get_entry(title)
    message=""
    if request.method == "POST":
        old_content = util.get_entry(title)
        content = request.POST["edit_content"]
        if util.save_entry(title, content):
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            util.save_entry(title, old_content)
            message="The content cannot be saved. Please check your syntax."
                
    return render(request, "encyclopedia/edit.html", {
        "message":message,
        "title":title,
        "content": content
    })

def create(request):
    message=""
    title=""
    content=""
    if request.method == "POST":
        title = request.POST["new_title"]
        content = request.POST["new_content"]
        if title != "":
            if util.show_entry(title) is None:
                if util.save_entry(title, content):
                    return HttpResponseRedirect(reverse("entry", args=(title,)))
                else:
                    message = "The content cannot be saved. Please check your syntax."
            else:
                message = "The file is already exist. Please change the title name or go to edit page."

    return render(request, "encyclopedia/create.html",{
        "message":message,
        "title":title,
        "content":content,
    })

def random(request):
    title = util.random_list()
    return HttpResponseRedirect(reverse("entry",args=(title,)))