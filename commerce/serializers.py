from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from commerce.models import Bid, Category, Comment, Listing, Watching, UserUploadedImage


class CommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.ReadOnlyField(source='id')
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    datetime = serializers.ReadOnlyField()
    listing = serializers.HyperlinkedRelatedField(
        lookup_field='listing_id', view_name='listings',
        read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'author', 'author_id', 'body', 'listing',
                  'listing_id', 'datetime']


class BidSerializer(serializers.ModelSerializer):
    creator_id = serializers.ReadOnlyField(source='creator.id')
    creator = serializers.ReadOnlyField(source='creator.username')

    def validate_listing_id(self, value):
        """
        Check that the listing_id exists and is active
        """
        try:
            listing = Listing.objects.get(pk=value.id)
        except Listing.DoesNotExist:
            raise serializers.ValidationError(
                "Listing does not exist.")

        if not listing.is_active:
            raise serializers.ValidationError(
                "Cannot bid on a closed listing.")

        return value

    def validate_bid_amount(self, value):
        """
        Check that the bid amount meets the minimum bid requirement
        """

        try:
            listing = Listing.objects.get(pk=self.initial_data['listing_id'])
        except Listing.DoesNotExist:
            return value

        if float(value) < listing.get_minimum_bid():
            raise serializers.ValidationError(
                "You must bid higher than the current bid amount.")
        return value

    class Meta:
        model = Bid
        fields = ['listing_id', 'creator', 'creator_id', 'bid_amount']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'listings']


class UserUploadedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserUploadedImage
        fields = ['id', 'creator', 'image_url']


class WatchingSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user_id.id')
    listing_id = serializers.ReadOnlyField(source='listing_id.id')
    class Meta:
        model = Watching
        fields = ['user_id', 'listing_id']


class UserWatchingSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        data = data.filter(
            user_id=self.context['request'].user, edition__hide=False)
        return super(UserWatchingSerializer, self).to_representation(data)

    class Meta:
        model = Watching
        fields = ['user_id', 'listing_id']


class ListingSerializer(serializers.ModelSerializer):
    def sort_bids_highest_to_lowest(self, instance):
        bids = instance.bids.order_by('-bid_amount')
        return BidSerializer(bids, many=True).data

    def followed_by_user(self, instance):
        user = self.context['request'].user
        listing_id = instance.id
        try:
            return user.watching.filter(listing_id=listing_id).exists()
        except Exception:
            return False

    # def followed_by_user(self, instance):
    #     user_id = self.context['request'].user.id
    #     listing_id = instance.id
    #     try:
    #         return Watching.objects.filter(user_id=user_id, listing_id=listing_id).exists()
    #     except:
    #         return False

    creator = serializers.ReadOnlyField(source='creator.username')
    creator_id = serializers.ReadOnlyField(source='creator.id')
    comments = CommentSerializer(many=True, required=False)
    bids = SerializerMethodField(method_name='sort_bids_highest_to_lowest')
    num_of_bids = serializers.ReadOnlyField(source='get_num_of_bids')
    num_of_unique_bids = serializers.ReadOnlyField(
        source='get_num_of_unique_bids')
    current_bid_price = serializers.ReadOnlyField(source='get_current_price')
    user_is_following = SerializerMethodField(method_name='followed_by_user')
    image_url = serializers.ImageField(required=False)


    class Meta:
        model = Listing
        extra_kwargs = {"category": {"error_messages": {
            "null": "Please select a category"}}}
        fields = ['id', 'creator', 'creator_id', 'title', 'description', 'start_bid',
                  'creation_date', 'is_active', 'winner', 'category', 'image_url', 'comments', 'bids', 'num_of_bids', 'num_of_unique_bids', 'current_bid_price', 'user_is_following']
