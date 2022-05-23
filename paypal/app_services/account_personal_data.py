from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from injector import inject

from paypal.domain.account.models import AccountPersonalData
from paypal.domain.account.repositories import AccountPersonalDataRepository
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectMustBeLinkedError,
    ObjectDoesNotExistError,
)
from paypal.domain.core.util import EntityVerbose
from paypal.app_services import PayPalAccountService


class AccountPersonalDataService:
    """ Account Personal Data service with basic CRUD. """

    @inject
    def __init__(
            self, repo: AccountPersonalDataRepository = AccountPersonalDataRepository()
    ):
        self.repo = repo
        super().__init__()

    def _check_if_email_exists(self, email: str) -> bool:
        obj = self.repo.get_by_email(email)
        return True if obj else False

    @classmethod
    def _link_corresponding_paypal_account(cls, data: dict) -> dict:
        account_id = data.get("account_id")
        if not account_id:
            raise ObjectMustBeLinkedError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA,
                link_to=[EntityVerbose.PAYPAL_ACCOUNT],
            )

        corresponding_paypal_account = PayPalAccountService().get_by_id(account_id)
        if not corresponding_paypal_account:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.PAYPAL_ACCOUNT,
                id=account_id
            )
        data["account"] = corresponding_paypal_account
        data.pop("account_id")
        return data

    def get_all(self) -> Optional[QuerySet[AccountPersonalData]]:
        return self.repo.get_all()

    def get_by_id(self, account_id: str) -> Optional[AccountPersonalData]:
        account_personal_data = self.repo.get_by_id(account_id)
        if not account_personal_data:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA, id=account_id
            )
        return account_personal_data

    def create(self, data: dict) -> AccountPersonalData:
        if self._check_if_email_exists(data.get("email")):
            raise ValidationError("This email is already used.")

        data = AccountPersonalDataService._link_corresponding_paypal_account(data)
        return self.repo.create(data)

    def update(self, account_id: str, data: dict) -> AccountPersonalData:
        if self._check_if_email_exists(data.get("email")):
            raise ValidationError("This email is already used.")

        account_personal_data = self.repo.get_by_id(account_id)
        if not account_personal_data:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA, id=account_id
            )
        return self.repo.update(account_personal_data, data)

    def delete(self, account_id: str) -> Optional[AccountPersonalData]:
        account_personal_data = self.repo.get_by_id(account_id)
        if not account_personal_data:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA, id=account_id
            )
        deleted_account_personal_data = self.repo.delete_obj(account_personal_data)
        if not deleted_account_personal_data:
            raise ObjectCannotBeDeletedError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA, id=account_id
            )
        else:
            return deleted_account_personal_data
