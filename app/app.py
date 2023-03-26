from aiohttp import web



def init_app(test=False) -> web.Application:
    app = web.Application()
    if test:
        from config import TestConfig as Config
    else:
        from config import Config

    from cleanups import close_db, close_test_db
    from startups import init_db, init_test_db

    app['config'] = Config

    if test:
        app.on_startup.append(init_test_db)
        app.on_cleanup.append(close_test_db)
    else:
        app.on_startup.append(init_db)
        app.on_cleanup.append(close_db)

    from api.user.routes import add_routes
    add_routes(app)

    from api.transaction.routes import add_routes
    add_routes(app)

    return app


