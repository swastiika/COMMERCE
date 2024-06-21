from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    imageurl = models.URLField(max_length=1000)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    watchlist = models.ManyToManyField(User,blank=True,null=True,related_name="listingWatchlist")
    def __str__(self):
        return self.title
class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    listing= models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"