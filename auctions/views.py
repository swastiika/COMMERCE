from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User,Listing,Bid,Comment,Category


def index(request):
    if request.method == "POST":
        cat = request.POST.get('category')
        if cat=="none":
            listings = Listing.objects.all()
        else:
            listings = Listing.objects.filter(category=cat)
    else:
            listings = Listing.objects.all()
    #    cat = request.GET.get('category')
    #    if cat:  # Check if cat is not None or empty
    #       listings = Listing.objects.filter(category__name=cat)
    # else:
    #     listings = Listing.objects.all()
    

    allCategory = Category.objects.all()
    return render(request, "auctions/index.html", {"listings":listings,"category":allCategory})


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


def create(request):
    if request.method=="POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        currentUser = request.user
        imageUrl = request.POST.get('url')
        bid = Bid(bid = float(price), user=currentUser)
        bid.save()
        new_listing = Listing(
            title=title,
            description = description,
            imageUrl = imageUrl,
            price = float(price),
            category  = category,
            owner = currentUser,
            created_at=timezone.now()
            
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:
        allCategory = Category.objects.all()
        return render(request,"auctions/create.html",{"category":allCategory})
    


def listing(request,id):
    list = Listing.objects.get(pk=id)
    iswatch = request.user in list.watchlist.all()
    bid_count = list.bids.count()
    is_active = list.is_active
    allcomments = Comment.objects.filter(listing = list)
    return render(request,"auctions/listing.html",{"listing":list,"iswatch":iswatch,"bidcount":bid_count,"user":request.user,"is_active":is_active,"comments":allcomments})



def addwatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id,)))


def removewatchlist(request,id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id,)))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingwatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings
    })


def placebid(request,id):
    bprice = request.GET.get('bidprice')
    listing = Listing.objects.get(pk=id)
    bid = Bid(bid = float(bprice), user=request.user,listing=listing)
    bid.save()

    message = "BID IS PLACED" 
    listing.price=float(bprice)
    listing.save()

    return render(request,"auctions/message.html",{
        "message":message
    })    



def closebid(request, id):
    listing = Listing.objects.get(pk=id)  # Fetch the listing
    highest_bid = Bid.objects.filter(listing=listing).order_by('-bid').first()  # Get the highest bid
    
    if highest_bid:  # If there is a highest bid
        listing.won = highest_bid.user  # Assign the winning user
    else:
        listing.won = None  # No bids, so no winner
    
    listing.is_active = False  # Mark the listing as closed
    listing.save()  # Save the changes
    
    return render(request, "auctions/winner.html", {
        "listing": listing,
    })

 
    

def closeview(request):
    listings = Listing.objects.filter(is_active=False)
    return render(request, "auctions/closed.html", {"listings": listings})

       


def addcomment(request,id):
    user = request.user
    message = request.POST.get('addcomment')
    listing = Listing.objects.get(pk=id)
    new_comment = Comment(
        author = user,
        message = message,
        listing = listing
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing",args=(id,)))