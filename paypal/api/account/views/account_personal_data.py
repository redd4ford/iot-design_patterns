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
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ViewSet

from paypal.api.account.serializers import (
    AccountPersonalDataOutputSerializer,
    AccountPersonalDataInputSerializer,
    AccountPersonalDataUpdateSerializer,
)
from paypal.app_services import AccountPersonalDataService
from paypal.domain.core.exceptions import (
    ObjectDoesNotExistError,
    ObjectCannotBeDeletedError,
    ObjectMustBeLinkedError,
)


class AccountPersonalDataViewSet(ViewSet):
    """
    Account Personal Data view.
    """
    GROUP_TAG = ["account details"]

    def __init__(
            self, service: AccountPersonalDataService = AccountPersonalDataService(),
            **kwargs
    ):
        super(AccountPersonalDataViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(AccountPersonalDataViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: AccountPersonalDataService = AccountPersonalDataService(),
            *args, **kwargs
    ):
        super(AccountPersonalDataViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=AccountPersonalDataOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
        },
        tags=GROUP_TAG
    )
    def retrieve(self, request, pk):
        """
        Get Account Personal Data.
        """
        try:
            account_personal_data = self.service.get_by_id(pk)

            output_serializer = AccountPersonalDataOutputSerializer(account_personal_data)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=AccountPersonalDataOutputSerializer(many=True)),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def list(self, request):
        """
        Get all Accounts Personal Data.
        """
        accounts_personal_data = self.service.get_all()

        output_serializer = AccountPersonalDataOutputSerializer(accounts_personal_data, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=None,
        request=AccountPersonalDataInputSerializer,
        responses={
            201: OpenApiResponse(response=AccountPersonalDataOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def create(self, request):
        """
        Create Account Personal Data.
        """
        incoming_data = AccountPersonalDataInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            account_personal_data = self.service.create(incoming_data.validated_data)

            output_serializer = AccountPersonalDataOutputSerializer(account_personal_data)
            return Response(output_serializer.data, status=HTTP_201_CREATED)
        except (ObjectDoesNotExistError, ObjectMustBeLinkedError, ValidationError) as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=AccountPersonalDataUpdateSerializer,
        responses={
            200: OpenApiResponse(response=AccountPersonalDataOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def update(self, request, pk):
        """
        Update Account Personal Data.
        """
        incoming_data = AccountPersonalDataUpdateSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            account_personal_data = self.service.update(pk, incoming_data.validated_data)

            output_serializer = AccountPersonalDataOutputSerializer(account_personal_data)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=AccountPersonalDataOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
            409: OpenApiResponse(description="Resource cannot be deleted: it has linked data")
        },
        tags=GROUP_TAG
    )
    def destroy(self, request, pk):
        """
        Delete Account Personal Data.
        """
        try:
            deleted_account_personal_data = self.service.delete(pk)

            output_serializer = AccountPersonalDataOutputSerializer(deleted_account_personal_data)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ObjectCannotBeDeletedError as e:
            return Response({"message": e.message}, status=HTTP_409_CONFLICT)
