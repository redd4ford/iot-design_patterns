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

from paypal.app_services import CsvLoaderService


class CsvLoaderAPIView(APIView):
    """
    CSV loader view set.
    """
    GROUP_TAG = ["api-csv"]

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
                "filename", OpenApiTypes.STR, OpenApiParameter.QUERY,
                required=False, default='generated.csv',
                description="Filename, should ALWAYS end with .csv"
            ),
            OpenApiParameter(
                "rows_to_create", OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=False, default=1000,
                description="Number of rows to create"
            ),
            OpenApiParameter(
                "flush_db",
                OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                required=False, default=False,
                description="Should the database tables be truncated?"
            ),
            OpenApiParameter(
                "regenerate_file_if_exists",
                OpenApiTypes.BOOL, OpenApiParameter.QUERY,
                required=False, default=False,
                description="If file with *filename* exists, should it be cleared first?"
            )
        ],
        request=None,
        responses={
            200: OpenApiResponse(response=HTTP_200_OK, description="Database is filled"),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=GROUP_TAG
    )
    def post(self, request):
        """
        Fills the database based on a generated CSV (also generates a CSV if it does not exist).
        """
        self.csv_loader_service.load(**request.query_params)
        return Response(
            {"message": "Database is filled"}, status=HTTP_200_OK
        )
