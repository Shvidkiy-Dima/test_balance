from aiohttp import web
from .views import add_transaction
from .views import get_transaction

async def create_user(request):
    ...
    return web.json_response({
        'id': ...,
        'name': ...,
    })


def add_routes(app):

    app.router.add_route('POST', r'/v1/transaction', add_transaction, name='add_transaction')
    app.router.add_route('GET', r'/v1/transaction/{uid}', get_transaction, name='incoming_transaction')
