from sqlalchemy import select

from marshmallow import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Transaction
from decimal import Decimal
from .serializers import TransactionSerializer

from aiohttp import web
from models import User, Transaction

async def add_transaction(request: web.Request):

    try:
        data = TransactionSerializer.load(await request.json())
    except ValidationError as err:
        return web.json_response(err.messages, status=400)

    async with AsyncSession(bind=request.app['db']) as session:
        usr, locked = await User.get_locked(data.get('user_id'), session)

        if usr is None:
            return web.json_response({"message": "Blocked by the transaction", 'code': 'locked'}, status=400)

        if locked:
            return web.json_response({'message': f'Account with id {data.get("user_id")} doesnt exists', 'code': 'not_found'}, status=400)

        if data['transaction_type'] == Transaction.TransactionType.WITHDRAW.value and usr.balance < Decimal(data.get('amount')):
            return web.json_response({"message": 'Lack of money', 'code': 'lack_of'}, status=402)

        if data['transaction_type'] == Transaction.TransactionType.DEPOSIT.value:
            usr.balance = usr.balance + Decimal(data['amount'])

        else:
            usr.balance = usr.balance - Decimal(data['amount'])

        tx = Transaction(**data)
        session.add(tx)
        session.add(usr)

        await session.commit()

    return web.json_response(status=200)


async def get_transaction(request: web.Request):
    transaction_uid: int = request.match_info['uid']

    async with AsyncSession(bind=request.app['db']) as session:
        transaction = (await session.execute(select(Transaction).where(Transaction.uid==transaction_uid))).scalar()

        if not transaction:
            return web.json_response(status=404)

        return web.json_response(TransactionSerializer.dump(transaction))