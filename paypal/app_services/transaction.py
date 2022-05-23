from typing import Optional

from django.db.models import QuerySet
from injector import inject

from paypal.domain.banking.models import Transaction
from paypal.domain.banking.repositories import TransactionRepository
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectDoesNotExistError,
    ObjectMustBeLinkedError,
)
from paypal.domain.core.util import EntityVerbose
from paypal.app_services.card import CardService


class TransactionService:
    """ Transaction service with basic CRUD. """

    @inject
    def __init__(self, repo: TransactionRepository = TransactionRepository()):
        self.repo = repo
        super().__init__()

    @classmethod
    def _link_corresponding_from_card(cls, data: dict, on_create: bool = False) -> dict:
        from_card_id = data.get("from_card_id")
        if on_create and not from_card_id:
            raise ObjectMustBeLinkedError(
                type=EntityVerbose.TRANSACTION,
                link_to=[f'from_card ({EntityVerbose.CARD})']
            )
        elif from_card_id:
            from_card = (
                CardService().get_by_id(from_card_id)
            )
            if not from_card:
                raise ObjectDoesNotExistError(
                    type=EntityVerbose.CARD,
                    id=from_card_id
                )
            data["from_card"] = from_card
            data.pop("from_card_id")
        return data

    @classmethod
    def _link_corresponding_to_card(cls, data: dict, on_create: bool = False) -> dict:
        to_card_id = data.get("to_card_id")
        if on_create and not to_card_id:
            raise ObjectMustBeLinkedError(
                type=EntityVerbose.TRANSACTION,
                link_to=[f'to_card ({EntityVerbose.CARD})']
            )
        elif to_card_id:
            to_card = (
                CardService().get_by_id(to_card_id)
            )
            if not to_card:
                raise ObjectDoesNotExistError(
                    type=EntityVerbose.CARD,
                    id=to_card_id
                )
            data["to_card"] = to_card
            data.pop("to_card_id")
        return data

    @classmethod
    def _link_objects(cls, data: dict, on_create: bool = False):
        data = TransactionService._link_corresponding_from_card(data, on_create)
        data = TransactionService._link_corresponding_to_card(data, on_create)
        return data

    def get_all(self) -> Optional[QuerySet[Transaction]]:
        return self.repo.get_all()

    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return self.repo.get_by_id(transaction_id)

    def get_related_to_card(self, card_id: str) -> Optional[QuerySet[Transaction]]:
        return self.repo.get_related_to_card(card_id=card_id)

    def get_by_from_card(self, from_card_id: str) -> Optional[QuerySet[Transaction]]:
        return self.repo.get_by_from_card(from_card_id=from_card_id)

    def get_by_to_card(self, to_card_id: str) -> Optional[QuerySet[Transaction]]:
        return self.repo.get_by_to_card(to_card_id=to_card_id)

    def get_by_account(self, account_id: str) -> Optional[QuerySet[Transaction]]:
        return self.repo.get_by_account(paypal_account_id=account_id)

    def create(self, data: dict) -> Transaction:
        data = TransactionService._link_objects(data, on_create=True)

        return self.repo.create(data)

    def update(self, transaction_id: str, data: dict) -> Transaction:
        transaction = self.repo.get_by_id(transaction_id)

        data = TransactionService._link_objects(data)

        return self.repo.update(transaction, data)

    def delete(self, transaction_id: str) -> Optional[Transaction]:
        transaction = self.repo.get_by_id(transaction_id)
        if not transaction:
            raise ObjectDoesNotExistError(
                type=EntityVerbose.TRANSACTION, id=transaction_id
            )
        deleted_transaction = self.repo.delete_obj(transaction)
        if not deleted_transaction:
            raise ObjectCannotBeDeletedError(
                type=EntityVerbose.TRANSACTION, id=transaction_id
            )
        else:
            return deleted_transaction
