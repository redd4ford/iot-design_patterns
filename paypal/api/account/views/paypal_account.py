from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from injector import inject
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ViewSet

from paypal.api.account.serializers import (
    PayPalAccountOutputSerializer,
    PayPalAccountInputSerializer,
    PayPalAccountUpdateSerializer
)
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectDoesNotExistError,
)
from paypal.app_services import PayPalAccountService


class PayPalAccountViewSet(ViewSet):
    GROUP_TAG = ["accounts"]

    """
    PayPal Account view.
    """

    def __init__(
            self, service: PayPalAccountService = PayPalAccountService(),
            **kwargs
    ):
        super(PayPalAccountViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(PayPalAccountViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: PayPalAccountService = PayPalAccountService(),
            *args, **kwargs
    ):
        super(PayPalAccountViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PayPalAccountOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
        },
        tags=GROUP_TAG
    )
    def retrieve(self, request, pk):
        """
        Get PayPal Account.
        """
        try:
            paypal_account = self.service.get_by_id(pk)

            output_serializer = PayPalAccountOutputSerializer(paypal_account)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=PayPalAccountOutputSerializer(many=True)),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def list(self, request):
        """
        Get all PayPal Accounts.
        """
        paypal_accounts = self.service.get_all()

        output_serializer = PayPalAccountOutputSerializer(paypal_accounts, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=None,
        request=PayPalAccountInputSerializer,
        responses={
            201: OpenApiResponse(response=PayPalAccountOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def create(self, request):
        """
        Create PayPal Account.
        """
        incoming_data = PayPalAccountInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            paypal_account = self.service.create(incoming_data.validated_data)

            output_serializer = PayPalAccountOutputSerializer(paypal_account)
            return Response(output_serializer.data, status=HTTP_201_CREATED)
        except (ObjectDoesNotExistError, ValidationError) as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=PayPalAccountUpdateSerializer,
        responses={
            200: OpenApiResponse(response=PayPalAccountOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
        },
        tags=GROUP_TAG
    )
    def update(self, request, pk):
        """
        Update PayPal Account.
        """
        incoming_data = PayPalAccountUpdateSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            paypal_account = self.service.update(pk, incoming_data.validated_data)

            output_serializer = PayPalAccountOutputSerializer(paypal_account)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PayPalAccountOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
            409: OpenApiResponse(description="Resource cannot be deleted: it has linked data")
        },
        tags=GROUP_TAG
    )
    def destroy(self, request, pk):
        """
        Delete PayPal Account.
        """
        try:
            deleted_paypal_account = self.service.delete(pk)

            output_serializer = PayPalAccountOutputSerializer(deleted_paypal_account)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ObjectCannotBeDeletedError as e:
            return Response({"message": e.message}, status=HTTP_409_CONFLICT)
