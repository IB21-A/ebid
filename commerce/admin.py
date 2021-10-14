from django.contrib import admin
from .models import Category, Listing, Comment, Bid, Watching

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "title", "category", "creation_date", "is_active")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "listing_id", "datetime")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "listing_id", "bid_amount")
    
class WatchingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "listing_id")

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watching, WatchingAdmin)