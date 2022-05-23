import uuid
from typing import Optional

from paypal.domain.account.models import (
    PayPalAccount,
    AccountPersonalData,
)
from paypal.domain.core.abstract import AbstractRepository
from paypal.domain.core.exceptions import (
    ObjectMustBeLinkedError
)
from paypal.domain.core.util import EntityVerbose


class PayPalAccountRepository(AbstractRepository):
    BASE_CLASS = PayPalAccount


class AccountPersonalDataRepository(AbstractRepository):
    BASE_CLASS = AccountPersonalData

    def get_by_id(self, object_id: str) -> Optional[BASE_CLASS]:
        try:
            return self.BASE_CLASS.objects.get(account__id=object_id)
        except self.BASE_CLASS.DoesNotExist:
            return None

    def get_by_email(self, email: str):
        try:
            return self.BASE_CLASS.objects.get(email__iexact=email)
        except self.BASE_CLASS.DoesNotExist:
            return None

    def create(self, data: dict) -> BASE_CLASS:
        if isinstance(data['account'], uuid.UUID):
            corresponding_paypal_account = (
                PayPalAccountRepository().get_by_id(f"{data['account']}")
            )
            if not corresponding_paypal_account:
                raise ObjectMustBeLinkedError(
                    type=self.BASE_CLASS._meta.verbose_name,
                    link_to=[EntityVerbose.PAYPAL_ACCOUNT],
                )
            data['account'] = corresponding_paypal_account
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj
