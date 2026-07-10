from pathlib import Path
from typing import Any, Literal
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.documents.seed import Seed
from app.schemas.internal.current import Current

dirname = Path(__file__).resolve().parent.parent


def inject_panel_context(request: Request) -> dict[str, Any]:
    current: Current | None = getattr(request.state, 'current', None)
    if current is None:
        return {}
    
    sort_key: Literal['recent', 'name'] = request.query_params.get('sortBy', 'recent')

    seeds = Seed.list_by(user_id=current.user.id)

    if sort_key == 'recent':
        seeds.sort(key = lambda s: s.created_at, reverse=True)
    elif sort_key == 'name':
        seeds.sort(key = lambda s: s.name)

    return {'seeds': seeds}


templates = Jinja2Templates(directory=dirname / 'views', context_processors=[inject_panel_context])
templates.env.globals['layout'] = lambda x: str(Path('layouts') / x)
templates.env.globals['partial'] = lambda x: str(Path('partials') / x)
templates.env.globals['macro'] = lambda x: str(Path('macros') / x)