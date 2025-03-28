from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing_detail(request, id):
    listData = Listing.objects.get(pk=id)
    isOwner = request.user.username == listData.author.username
    isWatchList = request.user in listData.watchlist.all()
    allComments = Comment.objects.filter(listing=listData)
    return render(request, "auctions/listdetail.html", {
        "listing": listData,
        "isWatchList":isWatchList, 
        "allComments": allComments,
        "isOwner": isOwner,
    })
    
    
def closeAuction(request, id):
    listData = Listing.objects.get(pk=id)
    listData.isactive = False
    listData.save()
    isWatchList = request.user in listData.watchlist.all()
    allComments = Comment.objects.filter(listing=listData)
    isOwner = request.user.username == listData.author.username
    return render(request, "auctions/listdetail.html", {
        "listing": listData,
        "isWatchList":isWatchList, 
        "allComments": allComments,
        "isOwner": isOwner,
        "message": "You closed the auction"
    })
    
def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    listData = Listing.objects.get(pk=id)
    isWatchList = request.user in listData.watchlist.all()
    allComments = Comment.objects.filter(listing=listData)
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(bidder=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listdetail.html", {
          "listing": listingData,
          "message": "Successful Bid", 
          "update" :True,
          "isWatchList":isWatchList, 
          "allComments": allComments,
        })
    else:
        return render(request, "auctions/listdetail.html", {
          "listing": listingData,
          "message": "Bid Failed", 
          "update" :False,
          "isWatchList":isWatchList, 
          "allComments": allComments,
        })


def displayWatchList(request):
    currentuser = request.user
    listings = currentuser.listingwatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings":listings,
    })


def addComment(request, id):
    currentuser = request.user
    listData = Listing.objects.get(pk=id)
    comment = request.POST['newComment']
    
    
    
    newComment = Comment(
        author=currentuser,
        listing=listData,
        textcontent=comment
    )
    
    newComment.save()
    listData = Listing.objects.get(pk=id)
    isWatchList = request.user in listData.watchlist.all()
    allComments = Comment.objects.filter(listing=listData)
    return render(request, "auctions/listdetail.html", {
        "listing": listData,
        "isWatchList":isWatchList, 
        "allComments": allComments,
    })
    
    
    


def removeWatchlist(request, id):
    listData = Listing.objects.get(pk=id)
    currentuser = request.user
    listData.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("list_detail", args=(id, )))


def addWatchlist(request, id):
     listData = Listing.objects.get(pk=id)
     currentuser = request.user
     listData.watchlist.add(currentuser)
     return HttpResponseRedirect(reverse("list_detail", args=(id, )))

def index(request):
    all_categories = Category.objects.all()
    activeListing = Listing.objects.filter(isactive=True)
    return render(request, "auctions/index.html", {
        "listings": activeListing,
        "categories": all_categories,
    })


def displaycategory(request):
    if request.method == "POST":
        categoryfromForm = request.POST["category"]
        category = Category.objects.get(categoryName=categoryfromForm)
        
        all_categories = Category.objects.all()
        activeListing = Listing.objects.filter(isactive=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": activeListing,
            "categories": all_categories,
        })

def createListing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories,
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.FILES["image"]
        
        
        currentuser = request.user
        
        categorydata = Category.objects.get(categoryName=category)
        
        bid = Bid(bid=float(price), bidder=currentuser)
        bid.save()
        
        #create new listing object
        newlisting = Listing(
            title=title,
            description=description,
            price=bid,
            category=categorydata,
            author=currentuser,
            image=image
        )
        newlisting.save()
        #insert into database
    
        #render
        return HttpResponseRedirect(reverse("index"))
        

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
