from rest_framework import serializers

from commerce.serializers import BidSerializer, CommentSerializer, ListingSerializer
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    listings = ListingSerializer(many=True)
    comments = CommentSerializer(many=True)
    bids = BidSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'listings', 'comments', 'bids']


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
