""" Constants file. """
from django.db import models


class AccountConstants:
    """
    User account constants.
    """

    class AccountTypes(models.TextChoices):
        PERSONAL = "personal", "Personal"
        BUSINESS = "business", "Business"
