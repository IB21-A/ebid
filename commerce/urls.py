from django.urls import path, include
from .views import ListingViewSet, CommentViewSet, BidViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('listings', ListingViewSet)
router.register('comments', CommentViewSet)
router.register('bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls))
]
