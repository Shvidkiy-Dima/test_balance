from aiohttp import web
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from dateutil.parser import parse
from models import User, Transaction


async def create_user(request: web.Request):

    async with AsyncSession(bind=request.app['db'], expire_on_commit=False) as session:

        name: str = (await request.json()).get('name')

        user = (await session.execute(select(User.id).where(User.name == name))).scalar()
        if user is not None:
            return web.json_response({'error': 'User already exists'}, status=400)


        user = User(name=name)
        session.add(user)
        await session.commit()

        return web.json_response({
            'id': user.id,
            'name': user.name,
        }, status=201)


async def get_user_balance(request: web.Request):
    user_id: int = int(request.match_info['id'])
    date: str = request.query.get('date')

    async with AsyncSession(bind=request.app['db']) as session:

        if date:
            date = parse(date)

            res = await session.execute(select(func.sum(Transaction.amount), Transaction.transaction_type).
                                        where(Transaction.user_id == user_id, Transaction.timestamp <= date).
                                        group_by(Transaction.transaction_type))

            res = {i['transaction_type']: i['sum'] for i in res.mappings().all()}
            return web.json_response({
                'balance':
                    str(res[Transaction.TransactionType.DEPOSIT.value] - res[Transaction.TransactionType.WITHDRAW.value])
            })

        usr_balance = await session.execute(select(User.balance).where(User.id==user_id))

        return web.json_response({
            'balance': str(usr_balance.scalar())
        })

