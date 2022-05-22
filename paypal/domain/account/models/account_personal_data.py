from django.core.validators import (
    MinLengthValidator,
    EmailValidator,
)
from django.db import models

from paypal.domain.account.models import PayPalAccount
from paypal.domain.core.util import EntityVerbose


class AccountPersonalData(models.Model):
    """
    Account personal data model.
    """

    account = models.OneToOneField(
        PayPalAccount,
        to_field='id', primary_key=True, on_delete=models.CASCADE, related_name="personal_data"
    )
    full_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)], blank=True)
    date_of_birth = models.DateField(blank=True)
    country = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(blank=True, upload_to="accounts/icons")
    password = models.CharField(max_length=48, validators=[MinLengthValidator(8)])
    email = models.EmailField(validators=[EmailValidator()], unique=True)

    REQUIRED_FIELDS = ['account', 'email', 'password']

    class Meta:
        verbose_name = EntityVerbose.ACCOUNT_PERSONAL_DATA
        verbose_name_plural = EntityVerbose.ACCOUNT_PERSONAL_DATA

    def __str__(self) -> str:
        return f'{self.account.id} | {self.full_name} {self.email}'

    @property
    def class_name(self) -> str:
        return self._meta.verbose_name
