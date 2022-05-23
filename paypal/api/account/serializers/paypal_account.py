""" Account related serializers. """
from rest_framework import serializers

from paypal.api.account.serializers import AccountPersonalDataOutputSerializer
from paypal.domain.account.models import (
    PayPalAccount,
)
from paypal.domain.core.exceptions import ObjectDoesNotExistError
from paypal.app_services import AccountPersonalDataService


class PayPalAccountOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalAccount
        fields = (
            "id",
            "created",
            "account_type",
            "balance",
            "details",
        )

    details = serializers.SerializerMethodField()

    @classmethod
    def get_details(cls, obj: PayPalAccount) -> dict:
        try:
            details = AccountPersonalDataService().get_by_id(obj.id)
            return AccountPersonalDataOutputSerializer(details).data
        except ObjectDoesNotExistError:
            return {}


class PayPalAccountInputSerializer(serializers.Serializer):
    account_type = serializers.CharField(required=True, allow_blank=False)
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, allow_null=False,
    )


class PayPalAccountUpdateSerializer(serializers.Serializer):
    account_type = serializers.CharField(required=False, allow_blank=False)
    balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=False,
    )
