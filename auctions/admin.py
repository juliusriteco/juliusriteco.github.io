from django.contrib import admin
from .models import AuctionListing, Category, Bidding, User
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bidding)
admin.site.register(User)