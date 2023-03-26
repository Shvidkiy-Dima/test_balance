from datetime import datetime
import requests
import uuid
from app.app import init_app


async def assert_balance(user, expected_balance, client, date=None):
    url = f'/v1/user/{user["id"]}'
    if date:
        url += f'?date={date}'
    balance_resp = await client.get(url)
    assert balance_resp.status == 200
    assert (await balance_resp.json())['balance'] == expected_balance



async def test_api(aiohttp_client):
    client = await aiohttp_client(init_app(test=True))
    user_resp = await client.post('/v1/user', json={
        'name': 'petya'
    })

    assert user_resp.status == 201
    user = await user_resp.json()
    assert user['id'] > 0
    assert user['name'] == 'petya'

    await assert_balance(user, '0.00', client)

    txn = {
        'user_id': user['id'],
        'uid': str(uuid.uuid4()),
        'type': 'DEPOSIT',
        'amount': '100.0',
        'timestamp': datetime(2023, 1, 4).isoformat(),  # technical field to make tests possible
    }
    txn_resp = await client.post('/v1/transaction', json=txn)
    assert txn_resp.status == 200
    await assert_balance(user, '100.00', client)

    detail_resp = await client.get(f'/v1/transaction/{txn["uid"]}')
    assert (await detail_resp.json())['type'] == 'DEPOSIT'
    assert (await detail_resp.json())['amount'] == '100.00'

    txn = {
        'user_id': user['id'],
        'uid': str(uuid.uuid4()),
        'type': 'WITHDRAW',
        'amount': '50.0',
        'timestamp': datetime(2023, 1, 5).isoformat(),  # technical field to make tests possible
    }
    txn_resp = await client.post('/v1/transaction', json=txn)
    assert txn_resp.status == 200
    await assert_balance(user, '50.00', client)


    txn = {
        'user_id': user['id'],
        'uid': str(uuid.uuid4()),
        'type': 'WITHDRAW',
        'amount': '60.0',
        'timestamp': datetime.utcnow().isoformat(),  # technical field to make tests possible
    }
    txn_resp = await client.post('/v1/transaction', json=txn)
    assert txn_resp.status == 402  # insufficient funds
    await assert_balance(user, '50.00', client)

    txn = {
        'user_id': user['id'],
        'uid': str(uuid.uuid4()),
        'type': 'WITHDRAW',
        'amount': '10.0',
        'timestamp': datetime(2023, 2, 5).isoformat(),  # technical field to make tests possible
    }
    txn_resp = await client.post('/v1/transaction', json=txn)
    assert txn_resp.status == 200
    await assert_balance(user, '40.00', client)
    await assert_balance(user, '50.00', client, date='2023-01-30T00:00:00.00000000')


