from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki",views.wiki_index, name="wiki_index"),
    path("wiki/create/",views.create, name="create"),
    path("wiki/edit/<title>", views.edit, name="edit"),
    path("wiki/search", views.search_index, name="search_index"),
    path("wiki/random/", views.random, name="random"),
    path("wiki/<title>",views.entry, name="entry"),
]
