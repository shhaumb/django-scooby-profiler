from django.http import HttpResponse

from .utils import get_backend


def get_data(request, uuid):
    backend = get_backend()
    json_data = backend.get(uuid) or ''
    backend.delete(uuid)
    return HttpResponse(json_data, content_type="application/json")


def get_cprofile_data(request, uuid):
    backend = get_backend()
    stats = backend.get(uuid + '-pstats')
    if stats is None:
        return HttpResponse('No stats found.')
    filename = request.GET['filename']
    response = HttpResponse(stats)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
