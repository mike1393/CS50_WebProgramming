from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE



class User(AbstractUser):
    profile_pic = models.ImageField(null=True, blank=True)
    def __str__(self):
        return f"{self.username}"

class Auction_list(models.Model):
    listing_name = models.CharField(max_length=64)
    listing_picture = models.ImageField(null=True, blank=True)
    category = models.ForeignKey("Category",on_delete=models.CASCADE,null=True, blank=True, related_name="listings")
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="purchases",null=True, blank=True)
    min_bid = models.DecimalField(max_digits=10, decimal_places=2)
    description =models.TextField(max_length=200, blank=True)
    is_open =  models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing_name}:{self.category} (by {self.owner} staring at ${self.min_bid})"
    
class Watchlist(models.Model):
    name = models.CharField(max_length=64, blank=True)
    owner = models.OneToOneField(User,on_delete=models.CASCADE, related_name="watchlists")
    listing = models.ManyToManyField(Auction_list,blank=True,related_name="watchedlists")

    def __str__(self):
        return f"{self.name} is being watched by {self.owner}"
class Meta:
        ordering = ['price']

class Category(models.Model):
    name = models.CharField(max_length=64, blank=True)
    picture = models.ImageField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class Bids(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Auction_list,on_delete=models.CASCADE,related_name="biddings")
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bidder} bids {self.price} on {self.listing}"
    class Meta:
        ordering = ['price']

class Comments(models.Model):
    content = models.TextField(max_length=200)
    timestamp = models.TimeField(auto_now=True)
    commentor = models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_list, on_delete=models.CASCADE,blank=True,null=True,related_name="comments")

    def __str__(self):
        return f"{self.content} (Replied by {self.commentor} at {self.timestamp} on {self.listing})"

class Replies(models.Model):
    content = models.TextField(max_length=100)
    timestamp = models.TimeField(auto_now=True)
    replier = models.ForeignKey(User,on_delete=models.CASCADE, related_name="replies")
    parent_comment = models.ForeignKey(Comments,on_delete=models.CASCADE,related_name="replies")

    def __str__(self):
        return f"{self.content} (Replied by {self.replier} at {self.timestamp} to {self.parent_comment})"