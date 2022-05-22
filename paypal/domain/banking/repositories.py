import uuid

from django.db.models import QuerySet, Q

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
from paypal.domain.core.repositories import AbstractRepository


class BillingAddressRepository(AbstractRepository):
    BASE_CLASS = BillingAddress

    def get_by_personal_data(self, personal_data: AccountPersonalData) -> QuerySet[BillingAddress]:
        return BillingAddress.objects.get(personal_data=personal_data)

    def create(self, data: dict) -> BillingAddress:
        if isinstance(data['account_personal_data'], uuid.UUID):
            data['account_personal_data'] = AccountPersonalDataRepository().get_by_id(
                f"{data['account_personal_data']}"
            )
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj


class CardRepository(AbstractRepository):
    BASE_CLASS = Card

    def get_by_account(self, paypal_account: PayPalAccount) -> QuerySet[Card]:
        return Card.objects.get(account=paypal_account)

    def get_preferred_by_account(self, paypal_account: PayPalAccount) -> Card:
        return Card.objects.get(account=paypal_account, is_preferred=True)

    def get_by_billing_address(self, billing_address: BillingAddress) -> QuerySet[Card]:
        return Card.objects.get(billing_address=billing_address)

    def get_by_billing_address_id(self, billing_address_id: str) -> QuerySet[Card]:
        return Card.objects.get(billing_address__id=billing_address_id)

    def create(self, data: dict) -> Card:
        if isinstance(data['account'], uuid.UUID):
            data['account'] = PayPalAccountRepository().get_by_id(
                f"{data['account']}"
            )
        if isinstance(data['billing_address'], uuid.UUID):
            data['billing_address'] = BillingAddressRepository().get_by_id(
                f"{data['billing_address']}"
            )
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj


class TransactionRepository(AbstractRepository):
    BASE_CLASS = Transaction

    def get_related_to_card(self, card: Card) -> QuerySet[Transaction]:
        return Transaction.objects.filter(
            Q(to_card=card) | Q(from_card=card)
        )

    def get_by_from_card(self, from_card: Card) -> QuerySet[Transaction]:
        return Transaction.objects.get(from_card=from_card)

    def get_by_to_card(self, to_card: Card) -> QuerySet[Transaction]:
        return Transaction.objects.get(to_card=to_card)

    def get_by_account(self, paypal_account: PayPalAccount) -> QuerySet[Transaction]:
        return Transaction.objects.get(to_card__account=paypal_account)

    def create(self, data: dict) -> Transaction:
        if isinstance(data['from_card'], uuid.UUID):
            data['from_card'] = CardRepository().get_by_id(f"{data['from_card']}")
        if isinstance(data['to_card'], uuid.UUID):
            data['to_card'] = CardRepository().get_by_id(f"{data['to_card']}")
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj
