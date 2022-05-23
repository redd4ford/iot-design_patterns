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


class AccountPersonalDataUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=16, required=False, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    password = serializers.CharField(required=False, allow_blank=False)
    email = serializers.EmailField(required=False, allow_blank=True)


class AccountPersonalDataInputSerializer(AccountPersonalDataUpdateSerializer):
    account_id = serializers.UUIDField(required=True, allow_null=False)
