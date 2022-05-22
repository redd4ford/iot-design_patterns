""" Constants file. """
from django.db import models


class TransactionConstants:
    """
    Transaction constants.
    """

    class PaymentMethods(models.TextChoices):
        PAYPAL_BALANCE = "paypal_balance", "PayPal_Balance"
        PAYMENT = "payment", "Payment"
        CARD = "card", "Card"
        REWARDS = "rewards", "Rewards"

    class TransactionStatuses(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class TransactionTypes(models.TextChoices):
        AUTO_PAYMENT = "auto_payment", "Auto_Payment"
        PAYMENT = "payment", "Payment"
        REFUND = "refund", "Refund"
        TRANSFER = "transfer", "Transfer"
