from django.views.decorators.http import require_http_methods

from apps.core.types import AppHttpRequest
from django.shortcuts import render

@require_http_methods(['GET'])
def index(request: AppHttpRequest):
    return render(request, 'core/index.html.j2')
