from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing,Category

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
    return render(request, "auctions/index.html",{
        "listings":activeListing
    })



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
