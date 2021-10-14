from rest_framework import serializers

from commerce.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Listing
        fields = '__all__'
