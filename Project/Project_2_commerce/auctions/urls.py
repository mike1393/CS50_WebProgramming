from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create,name="create"),
    path("category", views.category,name="category"),
    path("watchlist", views.my_watchlist,name="my_watchlist"),
    path("listing/<name>", views.listing,name="listing"),
    path("category/<cat_name>", views.category_search,name="category_search"),
    path("<username>/watchlist", views.my_watchlist_signed_in,name="my_watchlist_signed_in"),
    path("<username>/listing/<name>", views.listing_signed_in,name="listing_signed_in"),

    
]
