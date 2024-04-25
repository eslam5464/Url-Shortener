from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(
    directory=str(
        Path(__file__).resolve().parent.parent.parent.parent.joinpath(
            'frontend',
            'templates',
        )
    )
)
