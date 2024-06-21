from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing,Category,Comment

from .models import User
def createListing(request):
    if request.method == "GET":
        allcategories = Category.objects.all()
        return render(request, "auctions/create.html", {"categories": allcategories})
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        imageurl = request.POST.get("imageurl")
        price = request.POST.get("price")
        category = request.POST.get("category")
        category_name = Category.objects.get(category_name=category)

        new_listing = Listing(
            title=title,
            description=description,
            imageurl=imageurl,
            price=float(price),
            category=category_name,
            owner=request.user
        )
        new_listing.save()

    return HttpResponseRedirect(reverse("index"))

def createCategory(request):
    if request.method == "GET":
        return render(request, "auctions/category.html")
    else:
        category= request.POST.get("category")


        new_category =Category(
          category_name = category
        )
        new_category.save()

    return HttpResponseRedirect(reverse("index"))


def index(request):
    activeListing = Listing.objects.filter(is_active= True)
    allcategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListing,"category":allcategories
    })
def displaycat(request):
    if request.method=="POST":
        allcategories= Category.objects.all()
        categoryinput = request.POST['category']
        category = Category.objects.get(category_name=categoryinput)
        activeListing = Listing.objects.filter(is_active=True,category=category)
        return render(request,"auctions/index.html",{
            "listings":activeListing,"category": allcategories
        })
    

def listing(request,id):
    listingdata = Listing.objects.get(pk=id)
    isListingWatchlist = request.user in listingdata.watchlist.all()
    return render(request,"auctions/listing.html",{
        "listing":listingdata,"iswatch":isListingWatchlist
    })

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })


def removewatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))



def addwatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))
def login_view(request):
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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def addcomment(request,id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newcomment']
    newComment = Comment(
        author=currentUser,
        listing = listingData,
        message = message

    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing",args=(id )))