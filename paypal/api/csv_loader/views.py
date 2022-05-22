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

    def __init__(self, csv_loader_service: CsvLoaderService = CsvLoaderService(), *args, **kwargs):
        super(CsvLoaderAPIView, self).__init__(**kwargs)
        self.csv_loader_service = csv_loader_service

    def dispatch(self, request, *args, **kwargs):
        return super(CsvLoaderAPIView, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(self, request, csv_loader_service: CsvLoaderService = CsvLoaderService(), *args, **kwargs):
        super(CsvLoaderAPIView, self).setup(request, csv_loader_service, args, kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "filename", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False
            ),
            OpenApiParameter(
                "rows_to_create", OpenApiTypes.INT, OpenApiParameter.QUERY, required=False
            ),
            OpenApiParameter(
                "flush_db",
                OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                required=False, default=False
            ),
            OpenApiParameter(
                "regenerate_file_if_exists",
                OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                required=False, default=False
            )
        ],
        request=None,
        responses={
            200: OpenApiResponse(response=HTTP_200_OK, description="Database is filled"),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def post(self, request):
        """
        Fills the database based on a generated CSV (also generates a CSV if it does not exist).
        ###
            Parameters:
                - :filename: (str,def=generated.csv)            - should ALWAYS end with .csv
                - :rows_to_create: (int, def=1000)              - number of rows to create
                - :flush_db: (bool, def=False)                  - should database tables be
                                                                  truncated?
                - :regenerate_file_if_exists: (bool, def=False) - if file exists, should it be
                                                                  cleared first?
        """
        self.csv_loader_service.load(**request.query_params)
        return Response(
            {"message": "Database is filled"}, status=HTTP_200_OK
        )
