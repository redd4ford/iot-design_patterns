from typing import Optional

from django.db.models import QuerySet
from injector import inject

from paypal.domain.account.models import PayPalAccount
from paypal.domain.account.repositories import PayPalAccountRepository
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectDoesNotExistError,
)
from paypal.domain.core.util import EntityVerbose


class PayPalAccountService:
    """ PayPal Account service with basic CRUD. """

    @inject
    def __init__(self, repo: PayPalAccountRepository = PayPalAccountRepository()):
        self.repo = repo
        super().__init__()

    def get_all(self) -> Optional[QuerySet[PayPalAccount]]:
        return self.repo.get_all()

    def get_by_id(self, account_id: str) -> Optional[PayPalAccount]:
        paypal_account = self.repo.get_by_id(account_id)
        if not paypal_account:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.PAYPAL_ACCOUNT, id=account_id
            )
        return paypal_account

    def create(self, data: dict) -> PayPalAccount:
        return self.repo.create(data)

    def update(self, account_id: str, data: dict) -> PayPalAccount:
        paypal_account = self.repo.get_by_id(account_id)
        if not paypal_account:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.PAYPAL_ACCOUNT, id=account_id
            )
        return self.repo.update(paypal_account, data)

    def delete(self, account_id: str) -> Optional[PayPalAccount]:
        paypal_account = self.repo.get_by_id(account_id)
        if not paypal_account:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.PAYPAL_ACCOUNT, id=account_id
            )
        deleted_paypal_account = self.repo.delete_obj(paypal_account)
        if not deleted_paypal_account:
            raise ObjectCannotBeDeletedError(
                type=EntityVerbose.PAYPAL_ACCOUNT, id=account_id
            )
        else:
            return deleted_paypal_account
