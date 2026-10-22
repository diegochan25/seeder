from typing import TYPE_CHECKING
from django.http import HttpRequest

if TYPE_CHECKING:
    from apps.accounts.models import User


class AppHttpRequest(HttpRequest):
    user: 'User'