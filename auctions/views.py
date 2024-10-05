from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from PIL import Image

 
 
from .models import User, AuctionListing, Bidding, Category

class BiddingForm(forms.Form):
    newBid = forms.DecimalField(label="Bid")

class NewProductForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['name', 'description', 'image', 'category']

def toggle_watchlist(request, product_id):
    if request.method == "POST":
        user = request.user
        product = get_object_or_404(AuctionListing, pk=product_id)
        if product in user.watchlist.all():
            user.watchlist.remove(product)
        else:
            user.watchlist.add(product)
        
        return redirect('product_details', product_details_id=product_id)
    else:
        return HttpResponse("Ongeldige methode", status=405)
    
def disable(request, product_id):
    if request.method == "POST":
        user = request.user
        product = get_object_or_404(AuctionListing, pk=product_id)
        if user == product.owner:
            if product.isActive:
                product.isActive=False
                product.save()

                if product.image:
                    image_path = product.image.path
                    img = Image.open(image_path)
                    greyscale_img = img.convert('L')
                    greyscale_img.save(image_path)
                return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Ongeldige methode", status=405)
            

def New_bid(request, product_id):
    product = AuctionListing.objects.get(pk=product_id)
    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["newBid"]
            bid_amount = float(bid)
            if product.highest_bid is None or bid_amount > product.highest_bid.bid:
                new_bid = Bidding.objects.create(
                    auction_listing=product,
                    bidder=request.user,
                    bid=bid_amount,
                )
                product.highest_bid = new_bid
                product.save()
                return HttpResponseRedirect(reverse("product_details", args=[product_id]))
            else:
                return render(request, "auctions/product_details.html", {
                    "productDetails": product,
                    "BiddingForm": BiddingForm(),
                    "user": request.user,
                    "message": "Error: Bod moet hoger zijn dan het huidige hoogste bod.",
                })
        else:
            return HttpResponse("Ongeldige methode", status=405)
         
        
        



def index(request):
    return render(request, "auctions/index.html",{
        "products": AuctionListing.objects.all(),
    })

def createlisting(request):
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.owner = request.user
            auction_listing.save()
            return redirect('index')
    else: 
        form = NewProductForm()
    return render(request, "auctions/create.html",{
        "NewProductForm": form,
    })

def product_details(request, product_details_id):
    product = get_object_or_404(AuctionListing, id=product_details_id)

    return render(request, "auctions/product_details.html", {
        "productDetails": product,
        "BiddingForm": BiddingForm(),
        "user": request.user,  # Voeg de user toe aan de context
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
