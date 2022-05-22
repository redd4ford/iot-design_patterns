class EntityVerbose:
    """ Entity verbose names. """

    PAYPAL_ACCOUNT = "PayPal Account"
    ACCOUNT_PERSONAL_DATA = "Account Personal Data"
    BILLING_ADDRESS = "Billing Address"
    CARD = "Card"
    TRANSACTION = "Transaction"

    @classmethod
    def get_verbose_names(cls) -> list:
        """
        Return all verbose names as list.
        """
        return [
            EntityVerbose.PAYPAL_ACCOUNT,
            EntityVerbose.ACCOUNT_PERSONAL_DATA,
            EntityVerbose.BILLING_ADDRESS,
            EntityVerbose.CARD,
            EntityVerbose.TRANSACTION
        ]

    @classmethod
    def get_verbose_names_in_truncate_order(cls) -> list:
        """
        Return all verbose names in table truncate order as list.
        """
        return [
            EntityVerbose.TRANSACTION,
            EntityVerbose.CARD,
            EntityVerbose.BILLING_ADDRESS,
            EntityVerbose.ACCOUNT_PERSONAL_DATA,
            EntityVerbose.PAYPAL_ACCOUNT
        ]
