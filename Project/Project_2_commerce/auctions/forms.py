from django.db.models.base import Model
from django import forms
from django.forms import fields
from django.forms.fields import CharField



from .models import *

class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction_list
        exclude = ['owner']
        # fields = "__all__"
        
class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['price']

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']