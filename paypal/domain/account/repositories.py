import uuid

from django.core.exceptions import ValidationError

from paypal.domain.account.models import (
    PayPalAccount,
    AccountPersonalData,
)
from paypal.domain.core.repositories import AbstractRepository


class PayPalAccountRepository(AbstractRepository):
    BASE_CLASS = PayPalAccount


class AccountPersonalDataRepository(AbstractRepository):
    BASE_CLASS = AccountPersonalData

    def get_by_id(self, object_id: str) -> BASE_CLASS:
        try:
            return self.BASE_CLASS.objects.get(account__id=object_id)
        except self.BASE_CLASS.DoesNotExist:
            raise ValidationError(message=f"Object does not exist: {object_id}")

    def create(self, data: dict) -> AccountPersonalData:
        if isinstance(data['account'], uuid.UUID):
            data['account'] = PayPalAccountRepository().get_by_id(f"{data['account']}")
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj
