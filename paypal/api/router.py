from django.conf import settings
from django.conf.urls.static import static
from django.urls import (
    path,
    include,
)
from rest_framework_nested import routers

from paypal.api.account.views import (
    PayPalAccountViewSet,
    AccountPersonalDataViewSet,
)
from paypal.api.banking.views import (
    CardViewSet,
    BillingAddressViewSet,
    TransactionViewSet,
)
from paypal.api.csv_loader.views import CsvLoaderAPIView


router = routers.SimpleRouter()

# Accounts
router.register(r"accounts", PayPalAccountViewSet, basename="accounts")
router.register(r"details", AccountPersonalDataViewSet, basename="details")

# Banking
router.register(r"billing-addresses", BillingAddressViewSet, basename="billing_addresses")
router.register(r"cards", CardViewSet, basename="cards")
router.register(r"transactions", TransactionViewSet, basename="transactions")

# Url patterns
urlpatterns = [
    path(r"", include(router.urls)),
    path(
        r"csv-loader/load/",
        CsvLoaderAPIView.as_view(),
        name="csv_loader"
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
