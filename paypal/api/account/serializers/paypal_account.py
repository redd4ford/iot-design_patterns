""" Account related serializers. """
from rest_framework import serializers

from paypal.api.account.serializers import AccountPersonalDataOutputSerializer
from paypal.domain.account.models import (
    PayPalAccount,
)


class PayPalAccountOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalAccount
        fields = [
            "id",
            "created",
            "account_type",
            "balance",
        ]

    account_personal_data = AccountPersonalDataOutputSerializer()
