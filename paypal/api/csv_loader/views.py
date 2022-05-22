""" CSV related view sets. """
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from injector import inject
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from paypal.services.csv_loader import CsvLoaderService


class CsvLoaderAPIView(APIView):
    """
    CSV loader view set.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.csv_loader_service = None

    @inject
    def setup(self, request, csv_loader_service: CsvLoaderService, *args, **kwargs):
        self.csv_loader_service = csv_loader_service

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "filename", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False
            ),
            OpenApiParameter(
                "rows_to_create", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False
            ),
        ],
        request=None,
        responses={
            200: OpenApiResponse(response=HTTP_200_OK),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def post(self, request):
        """
        Fills the database based on a generated CSV (also generates a CSV if it does not exist).
        ###
            Parameters:
                - :filename: (str, not required) - generated.csv (should ALWAYS end with .csv!)
                - :rows_to_create: (int, not required) - 1000
        """
        self.csv_loader_service.load(**request.query_params)
        return Response("Database is filled", status=HTTP_200_OK)
