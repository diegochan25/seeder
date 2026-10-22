from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods
from apps.accounts.forms import SignIn

@require_http_methods(['GET', 'POST'])
def sign_in(request: HttpRequest):
    match (request.method):
        case 'GET':
            form = SignIn()
        case 'POST':
            form = SignIn(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(request, username=data['email'], password=data['password'])
                if user is not None:
                    login(request, user)
                    ttl = timedelta(days=(40 if data['remember_me'] else 8))
                    request.session.set_expiry(ttl)
                    intent = request.GET.get('next', 'schemas:index')
                    if not url_has_allowed_host_and_scheme(intent, allowed_hosts=settings.ALLOWED_HOSTS):
                        intent = 'schemas:index'
                    return redirect(intent)
                else:
                    messages.error(request, 'Please check your credentials and try again')
    return render(request, 'accounts/sign-in.html.j2', { 'form': form })

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

