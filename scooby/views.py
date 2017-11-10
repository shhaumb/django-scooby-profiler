from django.http import HttpResponse

from .utils import get_redis


def get_data(request, uuid):
    redis =  get_redis()
    return HttpResponse(
        redis.get(uuid) or '',
        content_type="application/json")
