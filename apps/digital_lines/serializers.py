from rest_framework import serializers
from .models import DigitalLineOrder


class DigitalLineOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = DigitalLineOrder
        fields = "__all__"