class CsvHeaders:
    """ CSV headers. """

    paypal_account_headers = [
        "id",
        "account_type",
        "balance"
    ]

    account_personal_data_headers = [
        "account",
        "full_name",
        "date_of_birth",
        "country",
        "phone_number",
        "avatar",
        "password",
        "email"
    ]

    billing_address_headers = [
        "id",
        "account_personal_data",
        "street_address",
        "additional_information",
        "center_of_population",
        "region",
        "zip_code"
    ]

    card_headers = [
        "id",
        "account",
        "billing_address",
        "balance",
        "is_preferred",
        "card_number",
        "cvv",
        "expiration_date"
    ]

    transaction_headers = [
        "id",
        "from_card",
        "to_card",
        "finished_at",
        "type",
        "payment_method",
        "status"
    ]

    @classmethod
    def get_headers(cls) -> list:
        """
        Return all headers as list.
        """
        return [
            CsvHeaders.paypal_account_headers,
            CsvHeaders.account_personal_data_headers,
            CsvHeaders.billing_address_headers,
            CsvHeaders.card_headers,
            CsvHeaders.transaction_headers
        ]
