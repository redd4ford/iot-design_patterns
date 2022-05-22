""" Account personal data serializers. """
from rest_framework import serializers

from paypal.domain.account.models import (
    AccountPersonalData,
)


class AccountPersonalDataOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPersonalData
        exclude = [
            "account",
            "password"
        ]
