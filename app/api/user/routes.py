from aiohttp import web
from api.user.views import create_user, get_user_balance


def add_routes(app):
    app.router.add_route('POST', r'/v1/user', create_user, name='create_user')
    app.router.add_route('GET', r'/v1/user/{id}', get_user_balance, name='get_user')
