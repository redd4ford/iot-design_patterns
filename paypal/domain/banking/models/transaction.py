from django.db import models

from paypal.domain.core.models import BaseUUIDModel
from paypal.domain.banking.models import Card
from paypal.domain.banking.constants import TransactionConstants
from paypal.domain.core.util import EntityVerbose


class Transaction(BaseUUIDModel):
    """
    Transaction model.
    """

    from_card = models.ForeignKey(
        Card, on_delete=models.DO_NOTHING, related_name="transaction_from"
    )
    to_card = models.ForeignKey(
        Card, on_delete=models.DO_NOTHING, related_name="transaction_to"
    )
    finished_at = models.DateTimeField()
    type = models.CharField(max_length=50, choices=TransactionConstants.TransactionTypes.choices)
    payment_method = models.CharField(
        max_length=50, choices=TransactionConstants.PaymentMethods.choices
    )
    status = models.CharField(
        max_length=50, choices=TransactionConstants.TransactionStatuses.choices
    )

    REQUIRED_FIELDS = ['from_card', 'to_card', 'type', 'payment_method', 'status']

    class Meta:
        verbose_name = EntityVerbose.TRANSACTION
        verbose_name_plural = f'{EntityVerbose.TRANSACTION}s'

    def __str__(self) -> str:
        return f'{self.id} | {self.from_card} -> {self.to_card} {self.status}'
