import csv
import uuid
from typing import Union

from injector import inject

from paypal.domain.core.util import EntityVerbose
from paypal.domain.csv_logic.util import CsvHeaders


class CsvConverterHandler:
    """ CSV data converter. """

    @classmethod
    def map_header_to_entity_name(cls, header: list) -> str:
        """
        Return entity verbose name based on headers.
        """
        headers = CsvHeaders().get_headers()
        entity_names = EntityVerbose().get_verbose_names()
        return {
            tuple(headers[i]): entity_names[i]
            for i in range(len(headers))
        }.get(tuple(header), None)

    @classmethod
    def convert_str_to_uuid(cls, value: Union[str, int]) -> Union[str, uuid.UUID]:
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
    def convert_row_to_dict(cls, header: list, row: list) -> dict:
        """
        Convert current row to a dict of column names and values.
        """
        return {
            header[j]: row[j]
            for j in range(len(row))
        }


class CsvReader:
    """ CSV file parser. """

    @inject
    def __init__(self, csv_converter: CsvConverterHandler = CsvConverterHandler()):
        self.csv_converter = csv_converter
        super().__init__()

    @classmethod
    def _is_row_a_header(cls, row: list) -> bool:
        """
        Check if current row is a header.
        """
        return row in CsvHeaders().get_headers()

    @classmethod
    def _is_row_blank(cls, row: list) -> bool:
        """
        Check if current row is blank.
        """
        return row[0] == '"'

    def parse(self, filename: str = 'generated.csv') -> dict:
        """
        Read CSV file and return a dictionary of rows related to specific models.
        """
        entity_names = EntityVerbose.get_verbose_names()
        result = {
            entity_names[i]: []
            for i in range(len(entity_names))
        }
        with open(f'{filename}', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            current_entity = None
            current_header = None
            current_entity_counter = 0

            for row in reader:
                if CsvReader._is_row_a_header(row):
                    if current_entity:
                        print(f'Found {current_entity_counter} entities of {current_entity}.')
                        current_entity_counter = 0

                    current_entity = self.csv_converter.map_header_to_entity_name(row)
                    current_header = row
                    print(f'Reading entities of class: {current_entity}...')
                elif not CsvReader._is_row_blank(row):
                    for i in range(len(row)):
                        row[i] = self.csv_converter.convert_str_to_uuid(row[i])

                    result[current_entity].append(
                        self.csv_converter.convert_row_to_dict(current_header, row)
                    )

                    current_entity_counter += 1
            print(f'Found {current_entity_counter} entities of {current_entity}.')

        return result
