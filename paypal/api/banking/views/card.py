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

from paypal.api.banking.serializers import (
    CardOutputSerializer,
    CardInputSerializer,
    CardUpdateSerializer,
)
from paypal.domain.core.exceptions import (
    ObjectCannotBeDeletedError,
    ObjectMustBeLinkedError,
    ObjectDoesNotExistError,
)
from paypal.app_services import CardService


class CardViewSet(ViewSet):
    """
    Card view.
    """
    GROUP_TAG = ["cards"]

    def __init__(
            self, service: CardService = CardService(),
            **kwargs
    ):
        super(CardViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(CardViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: CardService = CardService(),
            *args, **kwargs
    ):
        super(CardViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=CardOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
        },
        tags=GROUP_TAG
    )
    def retrieve(self, request, pk):
        """
        Get Card.
        """
        try:
            card = self.service.get_by_id(pk)

            output_serializer = CardOutputSerializer(card)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=CardOutputSerializer(many=True)),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def list(self, request):
        """
        Get all Cards.
        """
        cards = self.service.get_all()

        output_serializer = CardOutputSerializer(cards, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=None,
        request=CardInputSerializer,
        responses={
            200: OpenApiResponse(response=CardOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def create(self, request):
        """
        Create Card.
        """
        incoming_data = CardInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            card = self.service.create(incoming_data.validated_data)

            output_serializer = CardOutputSerializer(card)
            return Response(output_serializer.data, status=HTTP_201_CREATED)
        except (ObjectDoesNotExistError, ObjectMustBeLinkedError, ValidationError) as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=CardUpdateSerializer,
        responses={
            200: OpenApiResponse(response=CardOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
        },
        tags=GROUP_TAG
    )
    def update(self, request, pk):
        """
        Update Card.
        """
        incoming_data = CardUpdateSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            card = self.service.update(pk, incoming_data.validated_data)

            output_serializer = CardOutputSerializer(card)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"message": e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=CardOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Resource not found"),
            409: OpenApiResponse(description="Resource cannot be deleted: it has linked data")
        },
        tags=GROUP_TAG
    )
    def destroy(self, request, pk):
        """
        Delete Card.
        """
        try:
            deleted_card = self.service.delete(pk)

            output_serializer = CardOutputSerializer(deleted_card)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({"message": e.message}, status=HTTP_404_NOT_FOUND)
        except ObjectCannotBeDeletedError as e:
            return Response({"message": e.message}, status=HTTP_409_CONFLICT)
