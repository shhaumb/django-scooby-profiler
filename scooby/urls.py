from django.conf.urls import url

from .views import get_data, get_cprofile_data


urlpatterns = [
    url(r'^get-data/(?P<uuid>[\w\-]+)/$', get_data, name='scooby_get_data'),
    url(r'^get-cprofile-data/(?P<uuid>[\w\-]+)/$', get_cprofile_data,
        name='scooby_get_cprofile_data'),
]
