from django.core.validators import MinValueValidator
from django.db import models

from paypal.domain.account.constants import AccountConstants
from paypal.domain.core.models import BaseUUIDModel
from paypal.domain.core.util import EntityVerbose


class PayPalAccount(BaseUUIDModel):
    """
    Base PayPal account model.
    """

    account_type = models.CharField(max_length=50, choices=AccountConstants.AccountTypes.choices)
    balance = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=10, decimal_places=2
    )

    REQUIRED_FIELDS = ['account_type', 'balance']

    class Meta:
        verbose_name = EntityVerbose.PAYPAL_ACCOUNT
        verbose_name_plural = f'{EntityVerbose.PAYPAL_ACCOUNT}s'

    def __str__(self) -> str:
        return f'{self.id} | {self.account_type} {self.balance}'
