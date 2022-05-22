from django.core.validators import MaxValueValidator
from django.db import models

from paypal.domain.core.models import BaseUUIDModel
from paypal.domain.account.models import AccountPersonalData


class BillingAddress(BaseUUIDModel):
    """
    Billing address model.
    """

    account_personal_data = models.ForeignKey(
        AccountPersonalData, on_delete=models.CASCADE, related_name="address_account"
    )
    street_address = models.CharField(max_length=100)
    additional_information = models.TextField(max_length=1000, blank=True)
    center_of_population = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    zip_code = models.IntegerField(validators=[MaxValueValidator(9999999999)])

    REQUIRED_FIELDS = ['account', 'street_address', 'center_of_population', 'region', 'zip_code']

    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'

    def __str__(self) -> str:
        return (
            f'{self.account_personal_data.account.id} | '
            f'{self.account_personal_data.country} {self.region} {self.center_of_population} '
            f'({self.zip_code})'
        )
