from rest_framework import serializers
from .models import Order
import json

class OrderSerializer(serializers.ModelSerializer):
    parsed_raw_data = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"   # existing remains SAME

    def get_parsed_raw_data(self, obj):
        try:
            return json.loads(obj.raw_data)
        except Exception:
            return {}
