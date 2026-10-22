from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from apps.core.types import AppHttpRequest


@login_required
@require_http_methods(['GET', 'POST'])
def index(request: AppHttpRequest):
    match (request.method):
        case 'GET':
            pass
        case 'POST':
            pass

    return render(request, 'schemas/index.html.j2')


@login_required
@require_http_methods(['GET', 'PUT', 'PATCH', 'DELETE'])
def show(request: AppHttpRequest):
    match (request.method):
        case 'GET':
            pass
        case 'PUT' | 'PATCH':
            pass
        case 'DELETE':
            pass

@login_required
@require_http_methods(['GET'])
def new(request: AppHttpRequest):
    pass


@login_required
@require_http_methods(['GET'])
def edit(request: AppHttpRequest):
    pass