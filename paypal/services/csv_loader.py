import os

from injector import inject

from paypal.domain.account.models import (
    PayPalAccount,
    AccountPersonalData,
)
from paypal.domain.account.repositories import (
    PayPalAccountRepository,
    AccountPersonalDataRepository,
)
from paypal.domain.banking.models import (
    BillingAddress,
    Card,
    Transaction,
)
from paypal.domain.banking.repositories import (
    BillingAddressRepository,
    CardRepository,
    TransactionRepository,
)
from paypal.domain.csv_logic import (
    CsvGenerator,
    CsvReader,
)


class CsvLoaderService:
    """ Populate the database based on a generated fake data. """

    @inject
    def __init__(self, csv_generator: CsvGenerator, csv_reader: CsvReader):
        self.csv_generator = csv_generator
        self.csv_reader = csv_reader
        super().__init__()

    @classmethod
    def _map_class_name_to_repository(cls, class_name: str):
        """
        Return entity repository by class verbose name.
        """
        return {
            "PayPal Account": PayPalAccountRepository,
            "Account Personal Data": AccountPersonalDataRepository,
            "Billing Address": BillingAddressRepository,
            "Card": CardRepository,
            "Transaction": TransactionRepository
        }.get(class_name)

    @classmethod
    def _map_class_name_to_obj(cls, class_name: str):
        """
        Return entity class by class verbose name.
        """
        return {
            "PayPal Account": PayPalAccount,
            "Account Personal Data": AccountPersonalData,
            "Billing Address": BillingAddress,
            "Card": Card,
            "Transaction": Transaction
        }.get(class_name)

    def load(self, **query_params) -> None:
        """
        Generate CSV, parse it, and populate the database with data from the file.
        """
        filename = (
            query_params.get("filename")[0]
            if query_params.get("filename")
            else 'generated.csv'
        )
        rows_to_create = (
            int(query_params.get("rows_to_create")[0])
            if query_params.get("rows_to_create")
            else 1000
        )

        if not os.path.exists(f'../{filename}'):
            self.csv_generator.generate_csv(filename, rows_to_create)

        parsed_data = self.csv_reader.parse(filename)

        self.populate(parsed_data)

    def populate(self, parsed_data: dict) -> None:
        """
        Create entities and store them in the database.
        """
        print('Writing to DB...')
        for class_name, rows in parsed_data.items():
            print(class_name)
            repo = CsvLoaderService._map_class_name_to_repository(class_name)
            for row in rows:
                repo().create(row)
            print('OK')
        print('Database filled')
