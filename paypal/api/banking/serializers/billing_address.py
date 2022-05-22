from rest_framework import serializers

from paypal.domain.banking.models import BillingAddress


class BillingAddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'
