from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

async def init_db(app: web.Application):
    engine = create_async_engine(app['config'].DB_URI)
    app['db'] = engine


async def init_test_db(app: web.Application):
    from models import Base
    engine = create_async_engine(app['config'].DB_URI)
    app['db'] = engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)