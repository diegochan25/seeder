from pathlib import Path

from fastapi.templating import Jinja2Templates

dirname = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=dirname / 'views')
templates.env.globals['layout'] = lambda x: str(Path('layouts') / x)
templates.env.globals['partial'] = lambda x: str(Path('partials') / x)
templates.env.globals['macro'] = lambda x: str(Path('macros') / x)