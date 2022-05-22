import csv
import datetime
import random
import uuid

from faker import Faker

from paypal.domain.csv_logic.util import (
    paypal_account_headers,
    account_personal_data_headers,
    billing_address_headers,
    card_headers,
    transaction_headers,
)


class CsvGenerator:
    @classmethod
    def _generate_paypal_account_data(cls, new_id: uuid.UUID) -> list:
        """
        Generate values for an object of PayPalAccount and return them as a list.
        """
        return [
            new_id,
            random.choice(["personal", "business"]),
            round(random.uniform(0.0, 5000.0), 2),
        ]

    @classmethod
    def _get_unique_account_id(cls, account_ids: list, used_account_ids: set) -> uuid.UUID:
        """
        Find id of an account that does not have a linked AccountPersonalData object yet.
        """
        is_free = False
        new_id = None
        while not is_free:
            new_id = random.choice(account_ids)
            if new_id not in used_account_ids:
                is_free = True
        return new_id

    @classmethod
    def _generate_account_personal_data(cls, new_id: uuid.UUID) -> list:
        """
        Generate values for an object of AccountPersonalData and return them as a list.
        """
        return [
            new_id,
            Faker().name(),
            Faker().date_of_birth(),
            Faker().country(),
            Faker().msisdn(),
            "",
            Faker().password(),
            Faker().email()
        ]

    @classmethod
    def _generate_billing_address_data(cls, new_id: uuid.UUID, account_ids: list) -> list:
        """
        Generate values for an object of BillingAddress and return them as a list.
        """
        return [
            new_id,
            random.choice(account_ids),
            Faker().street_address(),
            Faker().sentence(),
            Faker().city(),
            Faker().state_abbr(),
            Faker().zipcode()
        ]

    @classmethod
    def _generate_card_data(
            cls, new_id: uuid.UUID, account_ids: list, billing_address_ids: list
    ) -> list:
        """
        Generate values for an object of Card and return them as a list.
        """
        return [
            new_id,
            random.choice(account_ids),
            random.choice(billing_address_ids),
            round(random.uniform(0.0, 50000.0), 2),
            False,
            Faker().credit_card_number(),
            Faker().credit_card_security_code(),
            Faker().credit_card_expire()
        ]

    @classmethod
    def _generate_transaction_data(cls, card_ids: list) -> list:
        """
        Generate values for an object of Transaction and return them as a list.
        """
        return [
            uuid.uuid4(),
            random.choice(card_ids),
            random.choice(card_ids),
            datetime.datetime.strftime(Faker().date_time_this_year(), "%Y-%m-%d %H:%M:%S"),
            random.choice(["auto_payment", "payment", "refund", "transfer"]),
            random.choice(["paypal_balance", "payment", "card", "rewards"]),
            random.choice(["pending", "completed", "cancelled"])
        ]

    @classmethod
    def generate_csv(cls, filename: str = 'generated.csv', rows_to_write: int = 1000) -> None:
        """
        Generate CSV file with fake data.
        """
        with open(f'../../{filename}', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            writer.writerow(paypal_account_headers)

            account_ids = []
            used_account_ids = set()

            for i in range(0, rows_to_write // 5):
                new_id = uuid.uuid4()
                account_ids.append(new_id)
                writer.writerow(
                    CsvGenerator._generate_paypal_account_data(new_id)
                )

            writer.writerow('\n')
            writer.writerow(account_personal_data_headers)

            for i in range(0, rows_to_write // 5):
                new_id = CsvGenerator._get_unique_account_id(account_ids, used_account_ids)
                used_account_ids.add(new_id)
                writer.writerow(
                    CsvGenerator._generate_account_personal_data(new_id)
                )

            writer.writerow('\n')
            writer.writerow(billing_address_headers)

            billing_address_ids = []
            for i in range(0, rows_to_write // 5):
                new_id = uuid.uuid4()
                billing_address_ids.append(new_id)
                writer.writerow(
                    CsvGenerator._generate_billing_address_data(new_id, account_ids)
                )

            writer.writerow('\n')
            writer.writerow(card_headers)

            card_ids = []
            for i in range(0, rows_to_write // 5):
                new_id = uuid.uuid4()
                card_ids.append(new_id)
                writer.writerow(
                    CsvGenerator._generate_card_data(new_id, account_ids, billing_address_ids)
                )

            writer.writerow('\n')
            writer.writerow(transaction_headers)

            for i in range(0, rows_to_write // 5):
                writer.writerow(
                    CsvGenerator._generate_transaction_data(card_ids)
                )

            print(f'Generated a CSV with {rows_to_write} rows.')


if __name__ == '__main__':
    CsvGenerator.generate_csv()
