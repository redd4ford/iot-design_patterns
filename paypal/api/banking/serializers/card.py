from rest_framework import serializers

from paypal.api.banking.serializers import BillingAddressOutputSerializer
from paypal.domain.banking.models import Card


class CardOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

    billing_address = BillingAddressOutputSerializer()
