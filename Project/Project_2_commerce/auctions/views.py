from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *


def index(request):
    page_title = "All Listings"
    categories = Category.objects.order_by("name")
    auction_list=Auction_list.objects.filter(is_open=True).order_by("listing_name")
    return render(request, "auctions/index.html",{
        "page_title":page_title,
        "categories":categories,
        "auction_list":auction_list,
    })

def category(request):
    page_title = "Categories"
    categories = Category.objects.order_by("name")
    auction_list=Auction_list.objects.filter(is_open=True).order_by("listing_name")
    return render(request, "auctions/category.html",{
        "page_title":page_title,
        "categories":categories,
        "auction_list":auction_list,
    })

def category_search(request,cat_name):
    page_title = cat_name
    categories = Category.objects.order_by("name")
    category_search = Category.objects.get(name=cat_name)
    auction_list=category_search.listings.order_by("listing_name")

    return render(request, "auctions/index.html",{
        "page_title":page_title,
        "categories":categories,
        "auction_list":auction_list,
    })

def my_watchlist(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("my_watchlist_signed_in",
        kwargs={
            'username': request.user.username,
            }))
    else:
        return HttpResponseRedirect(reverse("login"))



@login_required(login_url='login')
def my_watchlist_signed_in(request,username):
    watchlist = request.user.watchlists
    categories = Category.objects.order_by("name")
    page_title = f"Watchlist: {watchlist.name}"
    auction_list = watchlist.listing.order_by("listing_name")

    return render(request, "auctions/watchlist.html",{
        "page_title":page_title,
        "categories":categories,
        "auction_list":auction_list,
    })

def login_view(request):
    page_title = "Log in"
    categories = Category.objects.order_by("name")
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "page_title":page_title,
                "categories":categories,
                "error_message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html",{
            "page_title":page_title,
            "categories":categories,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    page_title = "Register"
    categories = Category.objects.order_by("name")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "page_title":page_title,
                "categories":categories,
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            watchlist = Watchlist.objects.create(name="My Favorite", owner=user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "page_title":page_title,
                "categories":categories,
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            "page_title":page_title,
            "categories":categories,
        })

@login_required(login_url='login')
def create(request):
    page_title = "Create Listing"
    categories = Category.objects.order_by("name")
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST,request.FILES)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.owner =request.user
            new_list.save()
    
    return render(request, "auctions/create.html",{
            "page_title":page_title,
            "categories":categories,
            "form":form
        })


def listing(request,name):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("listing_signed_in",
        kwargs={
            'username': request.user.username,
            'name': name,
            }))
    else:
        page_title = ""
        categories = Category.objects.order_by("name")
        listing = Auction_list.objects.get(listing_name=name)
        return render(request, "auctions/listing_not_signed_in.html",{
            "page_title":page_title,
            "categories":categories,
            "listing":listing,
        })

@login_required(login_url='login')
def listing_signed_in(request,username,name):
    if username != request.user.username:
        return HttpResponseRedirect(reverse("listing",
        kwargs={
            'name': name,
            }))
    else:
        page_title = ""
        success_message=""
        error_message=""
        categories = Category.objects.order_by("name")
        listing = Auction_list.objects.get(listing_name=name)
        comment_form = CommentForm()
        bidding_form = BiddingForm()
        if request.user == listing.winner and not listing.is_open:
            success_message="CONGRATS!!! You have won the listing!!!"
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment_form = comment_form.save(commit=False)
                new_comment_form.commentor =request.user
                new_comment_form.listing =listing
                new_comment_form.save()
            bidding_form = BiddingForm(request.POST)
            if bidding_form.is_valid():
                new_bidding_form = bidding_form.save(commit=False)
                condition1 = listing.biddings.count()==0 and new_bidding_form.price >= listing.min_bid
                condition2 = listing.biddings.count()>0 and new_bidding_form.price >= listing.biddings.last().price
                if condition1 or condition2:
                    new_bidding_form.bidder =request.user
                    new_bidding_form.listing =listing
                    print(f"{new_bidding_form.price}, type:{type(new_bidding_form.price)}, {new_bidding_form.price>listing.min_bid}")
                    success_message="The bid has been placed successfully."
                    new_bidding_form.save()
                    
                else:
                    if listing.biddings.count()==0:
                        error_message="The bid must be higher or equal than the starting price."
                    else:
                        error_message="The bid must be higher than the current price."
            print(request.POST.get("close_bid"))
            if request.POST.get("watchlist") == "add_to_list":
                request.user.watchlists.listing.add(listing)
                success_message="The listing has been added successfully."
            elif request.POST.get("watchlist") == "remove_list":
                request.user.watchlists.listing.remove(listing)
                success_message="The listing has been removed successfully."
            elif request.POST.get("close_bid") == "close_bid":
                if listing.owner == request.user:
                    listing.is_open=False
                    if listing.biddings.count()>0:
                        listing.winner = listing.biddings.last().bidder
                    listing.save()
                    success_message="The listing has been closed successfully."

        return render(request, "auctions/listing_signed_in.html",{
            "page_title":page_title,
            "success_message":success_message,
            "error_message":error_message,
            "categories":categories,
            "listing":listing,
            "comment_form":comment_form,
            "bidding_form":bidding_form,
        })
