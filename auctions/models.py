from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import *


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=80)
    
    
    def __str__(self):
        return self.categoryName
  
  

class Bid(models.Model):
    bid = models.FloatField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="userBid")
    
    
    def __str__(self):
        return self.bid
    
  
    
class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidprice")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    image = models.ImageField()
    isactive = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")
    
    
    def __str__(self):
        return self.title
    
    
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    textcontent = models.CharField(max_length=255)
    
    
    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    
    
    
