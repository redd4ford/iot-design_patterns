""" Billing address related serializers. """
from rest_framework import serializers

from paypal.domain.banking.models import BillingAddress


class BillingAddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'


class BillingAddressInputSerializer(serializers.Serializer):
    account_personal_data_id = serializers.UUIDField(required=True, allow_null=False)
    street_address = serializers.CharField(max_length=100, required=True, allow_blank=False)
    additional_information = serializers.CharField(
        max_length=1000, required=False, allow_blank=True
    )
    center_of_population = serializers.CharField(max_length=100, required=True, allow_blank=False)
    region = serializers.CharField(max_length=100, required=True, allow_blank=False)
    zip_code = serializers.IntegerField(required=True, allow_null=False)


class BillingAddressUpdateSerializer(serializers.Serializer):
    account_personal_data_id = serializers.UUIDField(required=False, allow_null=False)
    street_address = serializers.CharField(max_length=100, required=False, allow_blank=False)
    additional_information = serializers.CharField(
        max_length=1000, required=False, allow_blank=True
    )
    center_of_population = serializers.CharField(max_length=100, required=False, allow_blank=False)
    region = serializers.CharField(max_length=100, required=False, allow_blank=False)
    zip_code = serializers.IntegerField(required=False, allow_null=False)
