from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def sign_in(request: HttpRequest):
    match (request.method):
        case 'GET':
            pass
        case 'POST':
            pass

@require_http_methods(['GET', 'POST'])
def forgot_password(request: HttpRequest):
    match (request.method):
        case 'GET':
            pass
        case 'POST':
            pass

@require_http_methods(['GET', 'POST'])
def reset_password(request: HttpRequest):
    match (request.method):
        case 'GET':
            pass
        case 'POST':
            pass

