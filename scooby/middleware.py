import os
import jwt
import uuid
import cProfile
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

from .base import ScoobyData
from .utils import get_backend

from . import settings


class ScoobyMiddleware(MiddlewareMixin):
    def get_cookie_config(self, request):
        if not settings.SCOOBY_DEBUG:
            return
        encoded_jwt = request.COOKIES.get(settings.SCOOBY_COOKIE_NAME)
        if encoded_jwt is None:
            return
        try:
            return jwt.decode(encoded_jwt, settings.SCOOBY_SECRET_KEY)
        except:
            pass

    def process_request(self, request):
        cookie_config = self.get_cookie_config(request)
        if cookie_config is None or not cookie_config.get('enable'):
            return
        profiler = None
        if cookie_config.get('cprofile'):
            profiler = cProfile.Profile()
            profiler.enable()
        request.scooby_data = ScoobyData(profiler)
        request.scooby_data.on_process_request(request)

    def process_view(self, request, view, view_args, view_kwargs):
        cookie_config = self.get_cookie_config(request)
        if cookie_config is None or not cookie_config.get('enable'):
            return
        if hasattr(request, 'scooby_data'):
            request.scooby_data.on_process_view(
                request, view, view_args, view_kwargs)

    def process_response(self, request, response):
        cookie_config = self.get_cookie_config(request)
        if cookie_config is None or not cookie_config.get('enable'):
            return response
        if not hasattr(request, 'scooby_data'):
            return response
        request.scooby_data.on_process_response(request, response)
        unique_hex = uuid.uuid4().hex
        response['X-Scooby'] = unique_hex
        start = datetime.now()
        # Set data in backend for 2 mins.
        backend = get_backend()
        backend.set(unique_hex, request.scooby_data.as_json(), 120)
        if cookie_config.get('cprofile'):
            # Set cProfile stats in backend for 2 mins.
            profiler = request.scooby_data.profiler
            profiler.disable()
            temp_stats_filename = '/etc/%s.stats' % unique_hex
            profiler.dump_stats(temp_stats_filename)
            f = open(temp_stats_filename, 'rb')
            stats_key = unique_hex + '-pstats'
            backend.set(stats_key, f.read(), 120)
            f.close()
            os.remove(temp_stats_filename)
        end = datetime.now()
        time_taken = round((end - start).total_seconds() * 1000.0)
        response['X-Scooby-overhead'] = time_taken
        return response
