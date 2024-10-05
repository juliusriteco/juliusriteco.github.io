from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name='watchlisted_by')
    # Geen extra velden nodig tenzij je specifieke info voor de gebruiker wilt opslaan
    pass

    
class Category(models.Model): #niet meer aankomen. Meer categorieen niet nodig
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Gebruik ImageField voor de afbeelding
    highest_bid = models.ForeignKey('Bidding', null=True, blank=True, on_delete=models.SET_NULL, related_name="highest_bid_for")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    isActive = models.BooleanField(default=True)


    def __str__(self):
        return f"Product: {self.name}; Category: {self.category.name}; Highest Bid: {self.highest_bid.bid if self.highest_bid else 'No bid yet.'}; Owner: {self.owner}"
    
    def update_highest_bid(self):
        """Update the highest bid for the auction listing."""
        highest_bid = self.bids.order_by('-bid').first()  # Krijg het hoogste bod
        if highest_bid:
            self.highest_bid = highest_bid
            self.save()
    
class Bidding(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder.username} bid €{self.bid} on {self.auction_listing.name}"
