import uvloop
from aiohttp import web


import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def main() -> None:
    from app import init_app

    uvloop.install()
    app = init_app()
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)


if __name__ == '__main__':
    main()
