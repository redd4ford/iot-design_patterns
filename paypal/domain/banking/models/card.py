from datetime import datetime

from django.core.validators import (
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from paypal.domain.core.models import BaseUUIDModel
from paypal.domain.account.models import PayPalAccount
from paypal.domain.banking.models import BillingAddress
from paypal.domain.core.util import EntityVerbose


class Card(BaseUUIDModel):
    """
    Card model.
    """

    account = models.ForeignKey(
        PayPalAccount, on_delete=models.CASCADE, related_name="card_account"
    )
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, null=True, related_name="card_address"
    )
    balance = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=10, decimal_places=2
    )
    is_preferred = models.BooleanField(default=False)
    card_number = models.CharField(blank=False, max_length=30)
    cvv = models.CharField(
        blank=False, max_length=4,
        validators=[RegexValidator(r"^[0-9]{4}$", "CVV is incorrect.")]
    )
    expiration_date = models.CharField(
        blank=False, max_length=5,
        validators=[
            RegexValidator(r"^(0[1-9]|1[0-2])\/([0-9]{2})$", "expiration_date is incorrect.")
        ]
    )

    REQUIRED_FIELDS = [
        'account', 'balance', 'is_preferred', 'card_number', 'cvv', 'expiration_date'
    ]

    class Meta:
        verbose_name = EntityVerbose.CARD
        verbose_name_plural = f'{EntityVerbose.CARD}s'

    def __str__(self) -> str:
        return (
            f'{self.account.id} | {"*" if self.is_preferred else ""} '
            f'{self.card_number} {self.cvv} {self.expiration_date}'
        )

    @property
    def is_expired(self) -> bool:
        month, year = self.expiration_date.split()
        return datetime.strptime(f'01/{month}/{year} 00:00:00', '%d/%m/%Y %H:%M:%S') > datetime.now()
