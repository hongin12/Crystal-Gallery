from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError 
from django.contrib import auth 
from .models import User
from .models import Listing
from django.utils import timezone

def main(request):
    return render(request, "main.html")


def main2(request):
    return render(request, "main2.html")


#def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password) 
        if user is not None: 
            auth.login(request, user) 
            return redirect('main') 
        else: 
            return render(request, 'login.html', {'error': 'username or password is incorrect.'}) 
    else: 
        return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        
        return redirect('login')
    else:
        return render(request, "signup.html")

def mypage(request):
    return render(request, "mypage.html")

def mygallery(request):
    return render(request, "mygallery.html")

def auctionArts(request):
    listing = Listing.objects.all()
    return render(request, "auctionArts.html", {'listing' : listing})

def auction(request, listings_id):
    listings = get_object_or_404(Listing, pk=listings_id)
    return render(request, 'auction.html', {'listings':listings})

def auctionArts2(request):
    listing = Listing.objects.all()
    return render(request, "auctionArts2.html", {'listing' : listing})

def auctionArts3(request):
    listing = Listing.objects.all()
    return render(request, "auctionArts3.html", {'listing' : listing})

def about(request):
    return render(request, "about.html")

def bid(request):
    if request.method == "POST":
        new_bid = request.POST["bid"]
        item_id = request.POST["list_id"]

        item = Listing.objects.get(pk=item_id)
        old_bid = Bid.objects.filter(listing=item)

        if old_bid.count() < 1:
            bid = Bid(user=request.user, listing=item, highest_bid=new_bid)
            bid.save()
            messages.success(request, 'Bid Placed Successfully!', fail_silently=True)
        elif Decimal(new_bid) < old_bid[0].highest_bid:
            messages.warning(request, 'The bid you placed was lower than needed.', fail_silently=True)
        elif Decimal(new_bid) == old_bid[0].highest_bid:
            messages.warning(request, 'The bid you placed was the same as the current bid', fail_silently=True)
        else:
            old_bid = Bid.objects.get(listing=item)
            old_bid.highest_bid = new_bid
            old_bid.user = request.user
            old_bid.save()
            messages.success(request, 'Bid Placed Successfully!', fail_silently=True)
    return redirect("auctions:listing", item_id)

#def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect("main.html")
    return render(request, 'main.html')

def create(requset):
    new_listing = Listing()
    new_listing.name = requset.POST['name']
    new_listing.initial = requset.POST['initial']
    # new_listing.user = requset.POST['initial']
    new_listing.image = requset.POST['image']
    new_listing.created = timezone.now()
    new_listing.explain = requset.POST['explain']
    new_listing.save()
    return redirect('auctionArts')