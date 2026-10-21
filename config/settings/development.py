from pathlib import Path
from environ import Env

Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env.development')

from config.settings.base import *


DEBUG = True

INSTALLED_APPS += ['django_browser_reload']

MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']