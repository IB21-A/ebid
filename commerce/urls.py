from django.urls import path, include
from .views import ListingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
