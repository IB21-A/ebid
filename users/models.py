from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_active_listings(self):
        return self.listings.filter(is_active=True)

    def get_closed_listings(self):
        return self.listings.filter(is_active=False)

    def get_active_bids(self):
        # Returns only 1 result per listing_id with a bid
        unique_bids = self.bids.all().values_list('listing_id', flat=True).distinct()
        active_bids = [Listing.objects.get(
            pk=unique_id) for unique_id in unique_bids if Listing.objects.get(pk=unique_id).is_active]
        return active_bids

    def __str__(self):
        return f"{self.username}"
