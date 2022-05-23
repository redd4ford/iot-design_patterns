""" Transaction related serializers. """
from rest_framework import serializers

from paypal.domain.banking.models import Transaction


class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionInputSerializer(serializers.Serializer):
    from_card_id = serializers.UUIDField(required=True, allow_null=False)
    to_card_id = serializers.UUIDField(required=True, allow_null=False)
    type = serializers.CharField(max_length=50, required=True, allow_blank=False)
    payment_method = serializers.CharField(max_length=50, required=True, allow_blank=False)
    status = serializers.CharField(max_length=50, required=True, allow_blank=False)


class TransactionUpdateSerializer(serializers.Serializer):
    from_card_id = serializers.UUIDField(required=False, allow_null=False)
    to_card_id = serializers.UUIDField(required=False, allow_null=False)
    type = serializers.CharField(max_length=50, required=False, allow_blank=False)
    payment_method = serializers.CharField(max_length=50, required=False, allow_blank=False)
    status = serializers.CharField(max_length=50, required=False, allow_blank=False)
