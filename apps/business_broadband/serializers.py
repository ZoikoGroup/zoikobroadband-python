from rest_framework import serializers
from .models import BusinessBroadbandInquiry


class BusinessBroadbandInquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessBroadbandInquiry
        fields = '__all__'