from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_401_UNAUTHORIZED
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger.error(''.join(traceback.format_exception(
        etype=type(exc), value=exc, tb=exc.__traceback__)))
    if response:
        errors = []
        for field, value in response.data.items():
            if isinstance(value, list):
                value = value[0]
            errors.append(value)
        response.data = {}
        if hasattr(exc, 'code'):
            response.data['code'] = exc.code
        else:
            if response.status_code == HTTP_401_UNAUTHORIZED:
                response.data['code'] = response.status_code
            else:
                response.data['code'] = 400

        if hasattr(exc, 'detail'):
            response.data['message'] = exc.detail

        if len(errors) > 0:
            if isinstance(errors[0], dict):
                for key in errors[0]:
                    response.data['message'] = ''.join(errors[0][key]) + ': ' + key  # noqa
            else:
                response.data['message'] = errors[0]

            response.data['errors'] = errors

    return response


class CommonException(APIException):
    code = None
    detail = None

    def __init__(self, status_code=400, code=400,
                 detail='Common exception'):
        self.status_code = status_code
        self.code = code
        self.detail = detail
