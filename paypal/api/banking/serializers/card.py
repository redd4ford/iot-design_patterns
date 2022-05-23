""" Card related serializers. """
from rest_framework import serializers

from paypal.api.banking.serializers import BillingAddressOutputSerializer
from paypal.domain.banking.models import Card
from paypal.app_services import BillingAddressService
from paypal.domain.core.exceptions import ObjectDoesNotExistError


class CardOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            "id",
            "account_id",
            "created",
            "billing_address",
            "balance",
            "is_preferred",
            "card_number",
            "cvv",
            "expiration_date",
        )

    account_id = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()

    @classmethod
    def get_account_id(cls, obj: Card) -> str:
        return obj.account.id

    @classmethod
    def get_billing_address(cls, obj: Card) -> dict:
        try:
            billing_address = BillingAddressService().get_by_id(obj.id)
            return BillingAddressOutputSerializer(billing_address).data
        except ObjectDoesNotExistError:
            return {}


class CardInputSerializer(serializers.Serializer):
    account_id = serializers.UUIDField(required=True, allow_null=False)
    billing_address_id = serializers.UUIDField(required=False, allow_null=True)
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, allow_null=False
    )
    is_preferred = serializers.BooleanField(required=True, allow_null=False)
    card_number = serializers.CharField(max_length=30, required=True, allow_blank=False)
    cvv = serializers.CharField(max_length=4, required=True, allow_blank=False)
    expiration_date = serializers.CharField(max_length=5, required=True, allow_blank=False)


class CardUpdateSerializer(serializers.Serializer):
    account_id = serializers.UUIDField(required=False, allow_null=False)
    billing_address_id = serializers.UUIDField(required=False, allow_null=True)
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=False
    )
    is_preferred = serializers.BooleanField(required=False, allow_null=False)
