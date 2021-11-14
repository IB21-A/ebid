from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from .models import Bid, Category, Listing, Comment, Watching
from .serializers import BidSerializer, CategorySerializer, ListingSerializer, CommentSerializer, WatchingSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner

# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.order_by('-creation_date')
    serializer_class = ListingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# TODO add an admin or read only class
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class WatchingViewSet(viewsets.ModelViewSet):
    queryset = Watching.objects.all()
    serializer_class = WatchingSerializer
    permission_classes = [permissions.AllowAny]
