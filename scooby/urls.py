from django.conf.urls import url

from .views import get_data


urlpatterns = [
    url(r'^get-data/(?P<uuid>[\w\-]+)/$', get_data, name='scooby_get_data')
]
