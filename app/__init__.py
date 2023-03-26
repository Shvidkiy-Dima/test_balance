import sys
from pathlib import Path
from aiohttp import web

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# def create_app() -> web.Application:
#     from .app import init_app
#     app = init_app()
#     return app