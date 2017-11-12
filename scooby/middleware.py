import uuid

from django.conf import settings

from .base import ScoobyData
from .utils import get_redis


class ScoobyMiddleware(object):
    def process_request(self, request):
        if not settings.SCOOBY_DEBUG:
            return
        request.scooby_data = ScoobyData()
        request.scooby_data.on_process_request(request)

    def process_view(self, request, view, view_args, view_kwargs):
        if not settings.SCOOBY_DEBUG:
            return
        request.scooby_data.on_process_view(
            request, view, view_args, view_kwargs)

    def process_response(self, request, response):
        if not settings.SCOOBY_DEBUG:
            return response
        request.scooby_data.on_process_response(request, response)
        unique_hex = uuid.uuid4().hex
        response['X-Scooby'] = unique_hex
        # Set data in redis for 2 mins.
        redis = get_redis()
        redis.set(unique_hex, request.scooby_data.as_json(), 120)
        return response
