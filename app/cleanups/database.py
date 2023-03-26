from aiohttp import web
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql.ddl import DropTable


async def close_db(app: web.Application) -> None:

    engine: AsyncEngine = app['db']
    await engine.dispose()


from models import User, Transaction
async def close_test_db(app: web.Application) -> None:
    from config import TestConfig
    engine: AsyncEngine = app['db']

    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(Transaction.metadata.drop_all)
        print('Drop tables')

    await engine.dispose()
