from .models import User, Listing, Bid
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, make_naive

def increase_bid(user, auction):
    """
    Removes 5% base price per bid from user if previously also bidded, else total bid amount
    Creates a Bid record
    Increases the auction's number of bids
    
    Parameters
    ----------
    auction : class 'website.models.Auction
    """
    nBids = Bid.objects.filter(user_id = user).filter(auction_id = auction)      # bids the user has already placed in this auction

    currentCost = auction.base_price + auction.number_of_bids * 0.05 * auction.base_price
    if len(nBids)==0:
        toPay = currentCost
    else:
        lastBid = nBids.order_by('-bid_time')[0]
        nBids_prev = len(Bid.objects.filter(auction_id = auction).filter( bid_time__lt = lastBid.bid_time ))
        userPaid = auction.base_price + nBids_prev * 0.05 * auction.base_price
        toPay = currentCost - userPaid

    user.balance = float(user.balance) - toPay
    user.save()

    bid = Bid()
    bid.user_id = user
    bid.auction_id = auction
    bid.bid_time = timezone.localtime(timezone.now())
    bid.save()
    auction.number_of_bids += 1

    auction.save()

def remaining_time(auction):
    """
    Calculates the auction's remaining time
    in minutes and seconds and converts them 
    into a string.
    
    Parameters
    ----------
    auction : class 'website.models.Auction
    
    Returns
    -------
    
    time_left : str
        string representation of remaining time in
        minutes and seconds.
    expired : int
        if the value is less than zero then the auction ended.
    
    """
    time_left = make_naive(auction.time_ending) - datetime.now()            # timezone.now is supposed to be UTC time
    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_left = str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
    expired = days
    
    return time_left, expired


def update_balance(user):
    """
    Updates the balance of a user from all
    auctions where he didn't make the 
    winning bid (refunds all the bids)

    Parameters
    ----------
    user : class website.models.User

    """

    # number of auctions the user has bidded
    for auction in Auction.objects.all():

        if make_naive(auction.time_ending) < datetime.now():                                                                  # if auction is over

            bids = Bid.objects.filter(auction_id = auction.id).order_by('-bid_time')
            winningUser = bids[0].user_id.id

            if len(bids.filter(user_id = user.id)) != 0:
                if winningUser != user.id:

                    lastBid = bids.filter(user_id = user.id)[0]         #last bid done by user in that auction
                    nBids_prev = len(Bid.objects.filter(auction_id = auction).filter( bid_time__lt = lastBid.bid_time ))
                    userPaid = auction.base_price + nBids_prev * 0.05 * auction.base_price
                    user.balance = float(user.balance) + userPaid
                    user.save()

                    # now need to delete all records of the user bidding in that auction

                    Bid.objects.filter(auction_id = auction).filter(user_id = user.id).delete()

