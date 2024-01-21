from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    response_data = {
        'status_code': 0,
        'error_data': None,
    }

    if response is not None:
        response_data['error_data'] = str(response.data)
        response_data['status_code'] = response.status_code

        if isinstance(response.data, list) and isinstance(response.data[0], ErrorDetail):
            response_data['error_data'] = str(response.data[0])
            response_data['status_code'] = response.data[0].code

    return Response(response_data, status=response_data['status_code'])