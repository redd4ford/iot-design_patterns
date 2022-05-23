import uuid
from typing import Optional

from django.db.models import (
    QuerySet,
    Q,
)

from paypal.domain.account.models import (
    PayPalAccount,
    AccountPersonalData,
)
from paypal.domain.account.repositories import (
    AccountPersonalDataRepository,
    PayPalAccountRepository,
)
from paypal.domain.banking.models import (
    BillingAddress,
    Card,
    Transaction,
)
from paypal.domain.core.abstract import AbstractRepository
from paypal.domain.core.exceptions import (
    ObjectMustBeLinkedError,
)
from paypal.domain.core.util import EntityVerbose


class BillingAddressRepository(AbstractRepository):
    BASE_CLASS = BillingAddress

    def get_by_personal_data(
            self, personal_data: AccountPersonalData = None, personal_data_id: str = None
    ) -> Optional[QuerySet[BillingAddress]]:
        if personal_data:
            try:
                return BillingAddress.objects.get(account_personal_data=personal_data)
            except BillingAddress.DoesNotExist:
                return None
        elif personal_data_id:
            try:
                return BillingAddress.objects.get(
                    account_personal_data__account__id=personal_data_id
                )
            except BillingAddress.DoesNotExist:
                return None

    def create(self, data: dict) -> BillingAddress:
        if isinstance(data['account_personal_data'], uuid.UUID):
            account_personal_data = AccountPersonalDataRepository().get_by_id(
                f"{data['account_personal_data']}"
            )
            if not account_personal_data:
                raise ObjectMustBeLinkedError(
                    type=self.BASE_CLASS._meta.verbose_name,
                    link_to=[EntityVerbose.PAYPAL_ACCOUNT],
                )
            data['account_personal_data'] = account_personal_data

        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj


class CardRepository(AbstractRepository):
    BASE_CLASS = Card

    def get_by_account(
            self, paypal_account: PayPalAccount = None, paypal_account_id: str = None
    ) -> Optional[QuerySet[Card]]:
        if paypal_account:
            try:
                return Card.objects.get(account=paypal_account)
            except Card.DoesNotExist:
                return None
        elif paypal_account_id:
            try:
                return Card.objects.get(account__id=paypal_account_id)
            except Card.DoesNotExist:
                return None

    def get_preferred_by_account(
            self, paypal_account: PayPalAccount = None, paypal_account_id: str = None
    ) -> Optional[Card]:
        if paypal_account:
            try:
                return Card.objects.get(account=paypal_account, is_preferred=True)
            except Card.DoesNotExist:
                return None
        elif paypal_account_id:
            try:
                return Card.objects.get(account__id=paypal_account_id, is_preferred=True)
            except Card.DoesNotExist:
                return None

    def get_by_billing_address(
            self, billing_address: BillingAddress = None, billing_address_id: str = None
    ) -> Optional[QuerySet[Card]]:
        if billing_address:
            try:
                return Card.objects.get(billing_address=billing_address)
            except Card.DoesNotExist:
                return None
        elif billing_address_id:
            try:
                return Card.objects.get(billing_address__id=billing_address_id)
            except Card.DoesNotExist:
                return None

    def create(self, data: dict) -> Card:
        if isinstance(data['account'], uuid.UUID):
            account = PayPalAccountRepository().get_by_id(
                f"{data['account']}"
            )
            if not account:
                raise ObjectMustBeLinkedError(
                    type=self.BASE_CLASS._meta.verbose_name,
                    link_to=[EntityVerbose.PAYPAL_ACCOUNT],
                )
            data['account'] = account
        if isinstance(data['billing_address'], uuid.UUID):
            data['billing_address'] = BillingAddressRepository().get_by_id(
                f"{data['billing_address']}"
            )

        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj


class TransactionRepository(AbstractRepository):
    BASE_CLASS = Transaction

    def get_related_to_card(
            self, card: Card = None, card_id: str = None
    ) -> Optional[QuerySet[Transaction]]:
        if card:
            try:
                return Transaction.objects.filter(
                    Q(to_card=card) | Q(from_card=card)
                )
            except Transaction.DoesNotExist:
                return None
        elif card_id:
            try:
                return Transaction.objects.filter(
                    Q(to_card__id=card_id) | Q(from_card__id=card_id)
                )
            except Transaction.DoesNotExist:
                return None

    def get_by_from_card(
            self, from_card: Card = None, from_card_id: str = None
    ) -> Optional[QuerySet[Transaction]]:
        if from_card:
            try:
                return Transaction.objects.get(from_card=from_card)
            except Transaction.DoesNotExist:
                return None
        elif from_card_id:
            try:
                return Transaction.objects.get(from_card__id=from_card_id)
            except Transaction.DoesNotExist:
                return None

    def get_by_to_card(
            self, to_card: Card = None, to_card_id: str = None
    ) -> Optional[QuerySet[Transaction]]:
        if to_card:
            try:
                return Transaction.objects.get(to_card=to_card)
            except Transaction.DoesNotExist:
                return None
        elif to_card_id:
            try:
                return Transaction.objects.get(to_card__id=to_card_id)
            except Transaction.DoesNotExist:
                return None

    def get_by_account(
            self, paypal_account: PayPalAccount = None, paypal_account_id: str = None
    ) -> Optional[QuerySet[Transaction]]:
        if paypal_account:
            try:
                return Transaction.objects.get(to_card__account=paypal_account)
            except Transaction.DoesNotExist:
                return None
        elif paypal_account_id:
            try:
                return Transaction.objects.get(to_card__account__id=paypal_account_id)
            except Transaction.DoesNotExist:
                return None

    def create(self, data: dict) -> Transaction:
        if isinstance(data['from_card'], uuid.UUID):
            from_card = CardRepository().get_by_id(f"{data['from_card']}")
            if not from_card:
                raise ObjectMustBeLinkedError(
                    type=self.BASE_CLASS._meta.verbose_name,
                    link_to=['from_card'],
                )
            data['from_card'] = from_card
        if isinstance(data['to_card'], uuid.UUID):
            to_card = CardRepository().get_by_id(f"{data['to_card']}")
            if not to_card:
                ObjectMustBeLinkedError(
                    type=self.BASE_CLASS._meta.verbose_name,
                    link_to=['to_card'],
                )
            data['to_card'] = to_card

        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj
