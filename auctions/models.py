from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass



class Category(models.Model):
    category_name= models.CharField(max_length=50)

    def __str__(self):
        return self.category_name
    

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userBid")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="bids",null=True,blank=True)  
    

    def __str__(self):
        return f"{self.bid:.2f}"    

class Listing(models.Model):
    title = models.CharField(max_length=190)
    description = models.TextField(null=True)
    imageUrl = models.URLField(max_length=1000)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name="list_category")
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="listings")
    watchlist = models.ManyToManyField(User,blank=True,related_name="listingwatchlist")
    created_at = models.DateTimeField(blank=True,null=True) 
    winner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,name="won")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,null = True,blank=True,related_name="listingComment") 
    message = models.CharField(max_length=400) 


    def __str__(self):
        return f"{self.author} comment on {self.listing}"  