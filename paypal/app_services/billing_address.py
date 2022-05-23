from typing import Optional

from django.db.models import QuerySet
from injector import inject

from paypal.domain.banking.models import BillingAddress
from paypal.domain.banking.repositories import BillingAddressRepository
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectMustBeLinkedError,
    ObjectDoesNotExistError,
)
from paypal.domain.core.util import EntityVerbose
from paypal.app_services import AccountPersonalDataService


class BillingAddressService:
    """ Billing Address service with basic CRUD. """

    @inject
    def __init__(self, repo: BillingAddressRepository = BillingAddressRepository()):
        self.repo = repo
        super().__init__()

    @classmethod
    def _link_corresponding_personal_data(cls, data: dict, on_create: bool = False) -> dict:
        account_personal_data_id = data.get("account_personal_data_id")
        if on_create and not account_personal_data_id:
            raise ObjectMustBeLinkedError(
                type=EntityVerbose.BILLING_ADDRESS,
                link_to=[EntityVerbose.ACCOUNT_PERSONAL_DATA],
            )
        elif account_personal_data_id:
            corresponding_personal_data = (
                AccountPersonalDataService().get_by_id(account_personal_data_id)
            )
            if not corresponding_personal_data:
                raise ObjectDoesNotExistError(
                    type=EntityVerbose.ACCOUNT_PERSONAL_DATA,
                    id=account_personal_data_id
                )
            data["account_personal_data"] = corresponding_personal_data
            data.pop("account_personal_data_id")
        return data

    def get_all(self) -> Optional[QuerySet[BillingAddress]]:
        return self.repo.get_all()

    def get_by_id(self, billing_address_id: str) -> Optional[BillingAddress]:
        billing_address = self.repo.get_by_id(billing_address_id)
        if not billing_address:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.BILLING_ADDRESS, id=billing_address_id
            )
        return billing_address

    def get_by_account(self, account_id: str) -> Optional[QuerySet[BillingAddress]]:
        return self.repo.get_by_personal_data(personal_data_id=account_id)

    def create(self, data: dict) -> BillingAddress:
        data = BillingAddressService._link_corresponding_personal_data(data, on_create=True)
        return self.repo.create(data)

    def update(self, billing_address_id: str, data: dict) -> BillingAddress:
        billing_address = self.repo.get_by_id(billing_address_id)
        if not billing_address:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.BILLING_ADDRESS, id=billing_address_id
            )

        data = BillingAddressService._link_corresponding_personal_data(data)
        return self.repo.update(billing_address, data)

    def delete(self, billing_address_id: str) -> Optional[BillingAddress]:
        billing_address = self.repo.get_by_id(billing_address_id)
        if not billing_address:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.BILLING_ADDRESS, id=billing_address_id
            )
        deleted_billing_address = self.repo.delete_obj(billing_address)
        if not deleted_billing_address:
            raise ObjectCannotBeDeletedError(
                type=EntityVerbose.ACCOUNT_PERSONAL_DATA, id=billing_address_id
            )
        else:
            return deleted_billing_address
