from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import filters, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Bid, Category, Listing, Comment, UserUploadedImage, Watching
from .serializers import BidSerializer, CategorySerializer, ListingSerializer, CommentSerializer, WatchingSerializer, UserUploadedImageSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner
from .custom_helpers import get_object_or_None
from users.models import User
from rest_framework import status
from commerce_rest.settings import MEDIA_ROOT
import django_filters.rest_framework
# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.order_by('-creation_date')
    search_fields = ['title', 'description', 'category__name']
    # filter_backends = (filters.SearchFilter,)
    filter_backends = [filters.SearchFilter,
                       django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category', 'is_active']
    serializer_class = ListingSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # Debug Perform_create only
    # def perform_create(self, serializer):
    #     serializer.save(creator=User.objects.get(pk=1))


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


class UserImagesViewSet(viewsets.ModelViewSet):
    queryset = UserUploadedImage.objects.all()
    serializer_class = UserUploadedImageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    permission_classes = [
        permissions.AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)

    # Debug, DELETE ME
    def perform_create(self, serializer):
        serializer.save(creator=User.objects.get(pk=1))


class WatchingViewSet(viewsets.ModelViewSet):
    queryset = Watching.objects.all()
    serializer_class = WatchingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        user = request.user
        try:
            listing = Listing(id=request.data['listing_id'])
            instance = Watching(user_id=user, listing_id=listing)
        except Exception:
            return Response({"message": "Something went wrong. Check that user and listing exist"}, status=status.HTTP_400_BAD_REQUEST)

        watching_listing = get_object_or_None(
            Watching.objects.all(), user_id=request.user.id, listing_id=request.data['listing_id'])
        if watching_listing is None:
            serializer = WatchingSerializer(
                instance=instance, data=request.data)
            if serializer.is_valid():
                watching_saved = serializer.save()
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
