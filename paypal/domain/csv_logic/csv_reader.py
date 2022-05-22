import csv
import uuid

from paypal.domain.csv_logic.util import (
    paypal_account_headers,
    account_personal_data_headers,
    billing_address_headers,
    card_headers,
    transaction_headers,
)


class CsvReader:
    """ CSV file parser. """

    @classmethod
    def _is_row_a_header(cls, row: list):
        """
        Check if current row is a header.
        """
        return row in [
            paypal_account_headers,
            account_personal_data_headers,
            billing_address_headers,
            card_headers,
            transaction_headers
        ]

    @classmethod
    def _is_row_blank(cls, row: list):
        """
        Check if current row is blank
        """
        return row[0] == '"'

    @classmethod
    def _map_header_to_entity_name(cls, header: list):
        """
        Return entity verbose name based on headers.
        """
        return {
            tuple(paypal_account_headers): 'PayPal Account',
            tuple(account_personal_data_headers): 'Account Personal Data',
            tuple(billing_address_headers): 'Billing Address',
            tuple(card_headers): 'Card',
            tuple(transaction_headers): 'Transaction'
        }.get(tuple(header), None)

    @classmethod
    def _convert_str_to_uuid(cls, value):
        """
        Convert string UUIDs to UUID objects.
        """
        uuid_length = 36
        if isinstance(value, str) and len(value) == uuid_length:
            try:
                value = uuid.UUID(value)
            # since any string can contain 36 characters, need to check
            # if it is convertable to UUID
            except ValueError:
                pass
        return value

    @classmethod
    def _convert_row_to_dict(cls, header: list, row: list):
        """
        Convert row to a dict with column name and value.
        """
        return {
            header[j]: row[j]
            for j in range(len(row))
        }

    @classmethod
    def parse(cls, filename: str = 'generated.csv') -> dict:
        """
        Read CSV file and return a dictionary of rows related to specific models.
        """
        result = {
            'PayPal Account': [],
            'Account Personal Data': [],
            'Billing Address': [],
            'Card': [],
            'Transaction': []
        }
        with open(f'../../{filename}', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            current_entity = None
            current_header = None
            current_entity_counter = 0

            for row in reader:
                if CsvReader._is_row_a_header(row):
                    if current_entity:
                        print(f'Found {current_entity_counter} entities of {current_entity}.')
                        current_entity_counter = 0

                    current_entity = CsvReader._map_header_to_entity_name(row)
                    current_header = row
                    print(f'Reading entities of class: {current_entity}...')
                elif not CsvReader._is_row_blank(row):
                    for i in range(len(row)):
                        row[i] = CsvReader._convert_str_to_uuid(row[i])

                    result[current_entity].append(
                        CsvReader._convert_row_to_dict(current_header, row)
                    )

                    current_entity_counter += 1
            print(f'Found {current_entity_counter} entities of {current_entity}.')

        return result
