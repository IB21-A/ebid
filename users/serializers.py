from rest_framework import serializers

from commerce.serializers import BidSerializer, CommentSerializer, ListingSerializer, WatchingSerializer
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    listings = serializers.SerializerMethodField(
        method_name='sort_listings_by_descending_date')
    comments = CommentSerializer(many=True)
    bids = BidSerializer(many=True)
    # watching = WatchingSerializer(many=True)

    def sort_listings_by_descending_date(self, instance):
        listings = instance.listings.all().order_by('-creation_date')
        return ListingSerializer(listings, many=True).data

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'listings', 'comments', 'bids', 'watching']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We pass the "upper serializer" context to the "nested one"
        self.fields['listings'].context.update(self.context)
        self.fields['comments'].context.update(self.context)
        self.fields['bids'].context.update(self.context)




class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password',
                  'password_repeat', 'first_name', 'last_name', ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
        )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        user.set_password(validated_data['password'])
        user.save()

        return user
