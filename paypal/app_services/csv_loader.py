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
from paypal.domain.core.util import EntityVerbose
from paypal.domain.csv_logic import (
    CsvGenerator,
    CsvReader,
)


class CsvLoaderService:
    """ Populate the database based on a generated fake data. """

    @inject
    def __init__(
            self, csv_generator: CsvGenerator = CsvGenerator(), csv_reader: CsvReader = CsvReader()
    ):
        self.csv_generator = csv_generator
        self.csv_reader = csv_reader
        super().__init__()

    @classmethod
    def _map_class_name_to_repository(cls, class_name: str):
        """
        Return entity repository by class verbose name.
        """
        entity_verbose_names = EntityVerbose.get_verbose_names()
        entity_repos = [
            PayPalAccountRepository,
            AccountPersonalDataRepository,
            BillingAddressRepository,
            CardRepository,
            TransactionRepository
        ]
        return {
            entity_verbose_names[i]: entity_repos[i]
            for i in range(len(entity_repos))
        }.get(class_name)

    @classmethod
    def _map_class_name_to_obj(cls, class_name: str):
        """
        Return entity class by class verbose name.
        """
        entity_verbose_names = EntityVerbose.get_verbose_names()
        entity_classes = [PayPalAccount, AccountPersonalData, BillingAddress, Card, Transaction]
        return {
            entity_verbose_names[i]: entity_classes[i]
            for i in range(len(entity_classes))
        }.get(class_name)

    @classmethod
    def _parse_query_params(cls, **query_params) -> tuple:
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
        flush_db = (
            True if query_params.get("flush_db")[0] == 'true'
            else False
        )
        regenerate_file_if_exists = (
            True if query_params.get("regenerate_file_if_exists")[0] == 'true'
            else False
        )
        return filename, rows_to_create, flush_db, regenerate_file_if_exists

    def load(self, **query_params) -> None:
        """
        Generate CSV, parse it, and populate the database with data from the file.
        """
        filename, rows_to_create, flush_db, regenerate_file_if_exists = (
            CsvLoaderService._parse_query_params(**query_params)
        )

        if flush_db:
            for class_name in EntityVerbose.get_verbose_names_in_truncate_order():
                repo = CsvLoaderService._map_class_name_to_repository(class_name)
                repo().delete_all()
            print('Performed database reset.')

        if regenerate_file_if_exists:
            if os.path.exists(f'{filename}'):
                os.remove(f'{filename}')
                print(f'Removed previous {filename}.')

        if not os.path.exists(f'{filename}'):
            self.csv_generator.generate_csv(filename, rows_to_create)
        else:
            print(f'Found {filename}.')

        parsed_data = self.csv_reader.parse(filename)

        self.populate(parsed_data)

    def populate(self, parsed_data: dict) -> None:
        """
        Create entities and store them in the database.
        """
        print('Writing to DB...')
        for class_name, rows in parsed_data.items():
            repo = CsvLoaderService._map_class_name_to_repository(class_name)
            for row in rows:
                repo().create(row)
            print(f'{class_name} - OK')
        print('Database filled.')
