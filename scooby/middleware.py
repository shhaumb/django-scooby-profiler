import uuid

from .base import ScoobyData
from .utils import get_redis


class ScoobyMiddleware(object):
    def process_request(self, request):
        request.scooby_data = ScoobyData()
        request.scooby_data.on_process_request(request)

    def process_view(self, request, view, view_args, view_kwargs):
        request.scooby_data.on_process_view(
            request, view, view_args, view_kwargs)

    def process_response(self, request, response):
        request.scooby_data.on_process_response(request, response)
        unique_hex = uuid.uuid4().hex
        response['X-Scooby'] = unique_hex
        # Set data in redis for an hour.
        redis = get_redis()
        redis.set(unique_hex, request.scooby_data.as_json(), 3600)
        return response
