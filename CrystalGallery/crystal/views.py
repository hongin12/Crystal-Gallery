from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError 
from django.contrib import auth 
from .models import User
from .models import Listing
from django.contrib import messages
from decimal import *
from django.utils import timezone
from .forms import *
from .models import Bid
from .models import Comment
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from crystal.transactions import remaining_time


def main(request):
    return render(request, "main.html")

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
    #listing = Listing.objects.all()
    my_upload_arts= Listing.objects.all().filter(user=request.user)
    return render(request, "mygallery.html", {'my_upload_arts':my_upload_arts})

def auctionArts(request):
    listing = Listing.objects.all()
    bid = Bid.objects.all()
    highest_bid_art = Bid.objects.all().order_by('-highest_bid')[:3]
    
    return render(request, "auctionArts.html", {'listing' : bid, 'top1': highest_bid_art[0], 'top2': highest_bid_art[1], 'top3': highest_bid_art[2]})

def auction(request, listings_id):
    listings = get_object_or_404(Listing, pk=listings_id)
    bid = Bid.objects.get(listing=listings)
    comments = Comment.objects.filter(listing=listings)

    return render(request, 'auction.html', {'listings':listings, 'bid':bid, 'comments':comments})

def about(request):
    return render(request, "about.html")

def bid(request):
    if request.method == "POST":
        new_bid = request.POST["bid"]
        listings_id = request.POST["listings_id"]

        item = get_object_or_404(Listing, pk=listings_id)
        #이제 업데이트를 해야하는 Bid를 불러왔음.
        old_bid = Bid.objects.get(listing=item)
        old_bid.highest_bid = new_bid
        old_bid.user = request.user
        old_bid.save()
    return redirect("auctionArts")     
    

# def create(requset):
#      new_listing = Listing()
#      new_listing.name = requset.POST['name']
#      new_listing.initial = requset.POST['initial']
#      # new_listing.user = requset.POST['initial']
#      new_listing.display_picture = requset.POST['display_picture']
#      new_listing.explain = requset.POST['explain']
#      new_listing.time_ending = requset.POST['time_ending']
#      new_listing.save()
    
    
#return redirect('auctionArts')

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.display_picture = request.FILES['display_picture']
            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'error.html')
            user_pr.save()
            new_Bid = Bid()
            new_Bid.user = request.user
            new_Bid.listing = user_pr
            new_Bid.highest_bid = request.POST['initial']
            new_Bid.added = timezone.now()
            new_Bid.save()
            return render(request, 'details.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'create.html', context)

@login_required
def comment(request):
    if request.method == "POST":
        content = request.POST["content"]
        item_id = request.POST["list_id"]
        item = Listing.objects.get(pk=item_id)
        newComment = Comment(user=request.user, comment=content, listing=item)
        newComment.save()
        return redirect("auction", item_id)
    return redirect("main")
            