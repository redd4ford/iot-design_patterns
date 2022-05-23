from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from injector import inject

from paypal.domain.banking.models import Card
from paypal.domain.banking.repositories import CardRepository
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectDoesNotExistError,
    ObjectMustBeLinkedError,
)
from paypal.domain.core.util import EntityVerbose
from paypal.app_services.billing_address import BillingAddressService
from paypal.app_services.paypal_account import PayPalAccountService


class CardService:
    """ Card service with basic CRUD. """

    @inject
    def __init__(self, repo: CardRepository = CardRepository()):
        self.repo = repo
        super().__init__()

    def _check_if_preferred_card_exists(
            self, data: dict, current_card: Card = None, on_create: bool = False
    ) -> None:
        if data.get("is_preferred") is True:
            preferred_card = self.get_preferred_by_account(account_id=data.get("account_id"))
            if any([
                preferred_card and on_create,
                preferred_card and current_card and not on_create
                and preferred_card != current_card
            ]):
                raise ValidationError(message="A preferred card already exists!")

    @classmethod
    def _link_corresponding_paypal_account(cls, data: dict, on_create: bool = False) -> dict:
        account_id = data.get("account_id")
        if on_create and not account_id:
            raise ObjectMustBeLinkedError(
                type=EntityVerbose.CARD,
                link_to=[EntityVerbose.PAYPAL_ACCOUNT]
            )
        elif account_id:
            corresponding_paypal_account = (
                PayPalAccountService().get_by_id(account_id)
            )
            if not corresponding_paypal_account:
                raise ObjectDoesNotExistError(
                    type=EntityVerbose.PAYPAL_ACCOUNT,
                    id=account_id
                )
            data["account"] = corresponding_paypal_account
            data.pop("account_id")
        return data

    @classmethod
    def _link_corresponding_billing_address(cls, data: dict) -> dict:
        if billing_address_id := data.get("billing_address_id"):
            data["billing_address"] = BillingAddressService().get_by_id(billing_address_id)
            data.pop("billing_address_id")
        return data

    @classmethod
    def _link_objects(cls, data: dict, on_create: bool = False):
        data = CardService._link_corresponding_paypal_account(data, on_create)
        data = CardService._link_corresponding_billing_address(data)
        return data

    def get_all(self) -> Optional[QuerySet[Card]]:
        return self.repo.get_all()

    def get_by_id(self, card_id: str) -> Optional[Card]:
        card = self.repo.get_by_id(card_id)
        if not card:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.CARD, id=card_id
            )
        return card

    def get_by_account(self, account_id: str) -> Optional[QuerySet[Card]]:
        return self.repo.get_by_account(paypal_account_id=account_id)

    def get_preferred_by_account(self, account_id: str) -> Optional[Card]:
        return self.repo.get_preferred_by_account(paypal_account_id=account_id)

    def get_by_billing_address(self, billing_address_id: str) -> Optional[QuerySet[Card]]:
        return self.repo.get_by_billing_address(billing_address_id=billing_address_id)

    def create(self, data: dict) -> Card:
        self._check_if_preferred_card_exists(data, on_create=True)

        data = CardService._link_objects(data, on_create=True)

        return self.repo.create(data)

    def update(self, card_id: str, data: dict) -> Card:
        card = self.repo.get_by_id(card_id)
        self._check_if_preferred_card_exists(data, card)

        data = CardService._link_objects(data)

        return self.repo.update(card, data)

    def delete(self, card_id: str) -> Optional[Card]:
        card = self.repo.get_by_id(card_id)
        if not card:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.CARD, id=card_id
            )
        deleted_card = self.repo.delete_obj(card)
        if not deleted_card:
            raise ObjectCannotBeDeletedError(
                type=EntityVerbose.CARD, id=card_id
            )
        else:
            return deleted_card
