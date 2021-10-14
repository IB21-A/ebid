from django.db import models
from users.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(
        max_length=80, blank=False, null=False)
    image_url = models.URLField(blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="listings", blank=True, null=True)
    start_bid = models.DecimalField(max_digits=9, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="won", blank=True, null=True, default=None)

    def get_top_bid(self):
        if self.bids == None:
            return None

        from django.db.models import Max
        top_bid_amount = self.bids.aggregate(
            Max('bid_amount')).get("bid_amound__max")
        top_bid = self.bids.get(listing_id=self.id, bid_amount=top_bid_amount)
        return top_bid

    def get_num_of_bids(self):
        number_of_bids = self.bids.filter(listing_id=self.id).count()
        return number_of_bids

    def get_num_of_unique_bids(self):
        unique_bids = self.bids.filter(listing_id=self.id).values(
            'creator').distinct().count()
        return unique_bids

    def get_current_price(self):
        if self.get_num_of_bids() > 0:
            return self.get_top_bid().bid_amount
        else:
            return self.start_bid

    def get_minimum_bid(self):
        current_price = self.get_current_price()
        if current_price == self.start_bid and self.get_num_of_bids() == 0:
            return self.start_bid
        else:
            return float(current_price) + float(.01)

    def save(self, *args, **kwargs):
        if self.is_active == False:
            try:
                self.winner = self.get_top_bid().creator
            except Exception:
                self.winner = None

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    # max_length will not be enforced for textField but supposedly limits the text in the generated textarea widget
    body = models.TextField(max_length=300)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="comments")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.PROTECT, related_name="comments")
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"on {self.datetime}, {self.author} commented {self.body} on listing {self.listing_id}"


class Bid(models.Model):

    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="bids")
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.creator} ${self.bid_amount} bid on {self.listing_id}"


class Watching(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watching")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watching")
