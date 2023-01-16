from rest_framework import serializers


class StripeCheckoutSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    qty = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False)

    class Meta:
        fields = ["product_name", "price", "quantity", "qty"]