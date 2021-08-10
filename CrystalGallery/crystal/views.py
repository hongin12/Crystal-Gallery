from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError 
from django.contrib import auth 
from django.contrib.auth.models import User
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
from django.contrib import messages
import datetime
from datetime import datetime
from django.utils.dateformat import DateFormat
import time

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
            auth.login(request, user)
        except IntegrityError:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        
        return redirect('main')
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html', {'error':'username or password is incorrect'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('main')

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

#원래 bid
#def bid(request):
    if request.method == "POST":
        #새 응찰가
        new_bid = request.POST["new_highest_bid"]
        #해당 글 id - listing, bid id 둘다 받아오게 수정
        listing_id = request.POST["listing_id"]
        bid_id = request.POST["bid_id"]

        #bid찾는거 이렇게도 되나..?!모르겠음. -->오류남
        #updated_bid = get_object_or_404(Bid, pk=listing_id)
        updated_bid = get_object_or_404(Bid, pk=bid_id)
        
        
        updated_bid.user = request.user
        updated_bid.highest_bid = new_bid
        updated_bid.added = timezone.now()
        updated_bid.save()
        
    return redirect("auction", listing_id)
     
def bid(request):
    if request.method == "POST":
        # 오늘 날짜
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(Listing, pk=listing_id)
        deadline = listing.time_ending
        today = datetime.today().strftime("%Y%m%d")
        today = int(today)
        deadline = deadline.strftime("%Y%m%d")
        deadline = int(deadline)
        #새 응찰가
        new_bid = request.POST["new_highest_bid"]
        bid_id = request.POST["bid_id"]
        old_bid = get_object_or_404(Bid, pk=bid_id)
            
        if today > deadline :
            return render(request, "main.html")
        
        if request.user.coin >= int(new_bid)  and old_bid.highest_bid < int(new_bid) :
            
            # 1) 이전 최고가 응찰자 coin 반환
                # 이전 응찰자가 있는지 없는지 구분 : # 이전 응찰자가 아직 없을 때는 Bid객체의 user = 그림을 올린사람
            if old_bid.user != old_bid.listing.user:

                old_bid.user.coin = old_bid.user.coin + old_bid.highest_bid
                old_bid.user.save()


            # 2) 새로운 최고가 응찰자 coin 차감 & Bid 갱신
            request.user.coin = request.user.coin - int(new_bid) 
            request.user.save()
            old_bid.user = request.user
            old_bid.highest_bid = new_bid
            old_bid.added = timezone.now()
            old_bid.save()

    return redirect("auction", listing_id)



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
            user_pr.user = request.user

            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'error.html')
            user_pr.save()
            new_Bid = Bid()
            new_Bid.user = request.user
            
            request.user.coin = request.user.coin + 5000000
            request.user.save()

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
            