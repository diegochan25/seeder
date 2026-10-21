from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader, pass_context
from tailwind import get_config

ROOT = 'root'
TEMPLATE_DIRS = {ROOT: settings.BASE_DIR / 'templates'} | {
    d.parent.name: d for d in sorted(settings.BASE_DIR.glob('apps/*/templates'))
}


def _global(kind: str, relpath: str) -> str:
    return f"{ROOT}:{kind}/{relpath}"


def _local(context, kind: str, relpath: str) -> str:
    """Resolve within the templates dir of the app the calling template lives in."""
    filename = Path(context.environment.get_template(context.name).filename)
    for scope, directory in TEMPLATE_DIRS.items():
        if filename.is_relative_to(directory):
            prefix = '' if scope == ROOT else f"{scope}/"
            return f"{scope}:{prefix}{kind}/{relpath}"
    return _global(kind, relpath)


def global_icon(slug: str) -> str:
    return _global('icons', f"{slug}.svg.j2")


def global_layout(relpath: str) -> str:
    return _global('layouts', relpath)


def global_macro(relpath: str) -> str:
    return _global('macros', relpath)


def global_partial(relpath: str) -> str:
    return _global('partials', relpath)


@pass_context
def layout(context, relpath: str) -> str:
    return _local(context, 'layouts', relpath)


@pass_context
def macro(context, relpath: str) -> str:
    return _local(context, 'macros', relpath)


@pass_context
def partial(context, relpath: str) -> str:
    return _local(context, 'partials', relpath)


def tailwind_css():
    href = staticfiles_storage.url(get_config('TAILWIND_CSS_PATH'))
    return format_html('<link rel="stylesheet" href="{}">', href)

def environment(**options):
    options['loader'] = ChoiceLoader([
        options['loader'],
        PrefixLoader({k: FileSystemLoader(v) for k, v in TEMPLATE_DIRS.items()}, delimiter=':'),
    ])
    env = Environment(**options)
    env.globals.update(
        static=staticfiles_storage.url,
        url=reverse,
        tailwind_css=tailwind_css,
        now=now,
        global_icon=global_icon,
        global_layout=global_layout,
        global_macro=global_macro,
        global_partial=global_partial,
        layout=layout,
        macro=macro,
        partial=partial,
        DEBUG=settings.DEBUG,
    )
    return env