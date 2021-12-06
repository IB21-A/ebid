from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework import permissions
from rest_framework import status
from .models import Bid, Category, Listing, Comment, Watching
from .serializers import BidSerializer, CategorySerializer, ListingSerializer, CommentSerializer, WatchingSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner
from .custom_helpers import get_object_or_None


# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    search_fields = ['title','description']
    filter_backends = (filters.SearchFilter,)
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
    queryset = Category.objects.order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    pagination_class = None


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

    def create(self, request):
        user = request.user

        listing = Listing(id=request.data['listing_id'])
        instance = Watching(user_id=user, listing_id=listing)
        watching_listing = get_object_or_None(
            Watching.objects.all(), user_id=request.user.id, listing_id=request.data['listing_id'])
        if watching_listing is None:
            serializer = WatchingSerializer(
                instance=instance, data=request.data)
            if serializer.is_valid():
                watching_saved = serializer.save()
                print(watching_saved)
                return Response({"message": f"{watching_saved.listing_id.id} added to watch list"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        # TODO refactor into destroy()
        watching_listing.delete()

        return Response({"message": f"{watching_listing.listing_id} removed from watch list"}, status=status.HTTP_200_OK)

    # def destroy(self, request):
    #     user_id = request.user.id
    #     print(request.user)
    #     # listing = Listing(id=request.data['listing_id'])
    #     watching_listing = get_object_or_None(
    #         Watching.objects.all(), user_id=user_id, listing_id=request.data['listing_id'])

    #     if watching_listing is None:
    #         return Response({"message": f"User is already not currently watching {watching_listing.listing_id}"}, status=status.HTTP_400_BAD_REQUEST)

    #     watching_listing.delete()
    #     return Response({"message": f"{watching_listing.listing_id} removed from watch list"}, status=status.HTTP_200_OK)
