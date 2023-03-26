import os
import string
import sys
import random
import logging
import time
import decimal
from pathlib import Path
from functools import partial
import requests
import multiprocessing
from multiprocessing.pool import Pool as ProcessPool
from multiprocessing.pool import ThreadPool
from uuid import uuid4
from datetime import datetime
import requests
from decimal import Decimal

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ['SETTINGS_CONFIGURATION'] = 'test'

from aiohttp import web

from app.app import init_app

API_URL = f'http://{"localhost"}:{"8000"}'

def _start_test_serv():
    app = init_app(test=True)
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)


def _req_to_api(n, user_id,  *args, **kwargs):
    amount = round(decimal.Decimal(random.choice(range(10, 10000)) / 100), 2)

    method = random.choice(['deposit', 'withdraw'])

    data = {
        'user_id': user_id,
        'uid': str(uuid4()),
        'type': method.upper(),
        'amount': str(amount),
        'timestamp': datetime.utcnow().isoformat(),  # technical field to make tests possible
    }

    res = requests.post(f'{API_URL}/v1/transaction', json=data)

    if res.status_code == 400 and res.json().get('code') == 'locked':
        return _req_to_api(n, user_id, method)

    if res.status_code == 402 and res.json().get('code') == 'lack_of':
        return None, method

    return (-amount if method == 'withdraw' else amount), method


def _test_concurrency():

    threads_count = random.choice(range(80, 100))
    print(f'Threads {threads_count}')

    res = requests.post(f'{API_URL}/v1/user', json={
        'name':  ''.join(random.choice(string.ascii_letters) for i in range(10))
    })

    user_id = res.json()['id']

    with ThreadPool() as pool:

        fnc = partial(_req_to_api, user_id=user_id)
        res = pool.map(fnc, range(threads_count))

        result_balance = sum(amount for amount, method in res if amount is not None)

        current_balance = requests.get(f'{API_URL}/v1/user/{user_id}').json()['balance']

        print(result_balance, current_balance)
        assert Decimal(current_balance) == Decimal(result_balance)


def test_account():
    server_proc = multiprocessing.Process(target=_start_test_serv)
    server_proc.start()
    time.sleep(2)

    try:
        _test_concurrency()
    finally:
        print('-' * 100)
        server_proc.terminate()
        server_proc.join()


