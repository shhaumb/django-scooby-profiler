from django.http import HttpResponse

from .utils import get_redis


def get_data(request, uuid):
    redis =  get_redis()
    json_data = redis.get(uuid) or ''
    redis.delete(uuid)
    return HttpResponse(json_data, content_type="application/json")
