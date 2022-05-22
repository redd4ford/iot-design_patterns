from django.contrib import admin

from paypal.domain.account.models import (
    PayPalAccount,
    AccountPersonalData,
)
from paypal.domain.banking.models import (
    BillingAddress,
    Card,
    Transaction,
)

admin.site.register(PayPalAccount)
admin.site.register(AccountPersonalData)
admin.site.register(BillingAddress)

admin.site.register(Card)
admin.site.register(Transaction)
