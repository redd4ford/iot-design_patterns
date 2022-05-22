from rest_framework import serializers

from paypal.domain.banking.models import Transaction


class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
