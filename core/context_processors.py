from typing import Union

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest

from core import settings


def main_context_processor(_: Union[WSGIRequest, ASGIRequest]):
    return {
        'debug': settings.DEBUG
    }
