#!/bin/bash

python /app/check_conn.py --service-name db --port 5432  --ip db

alembic upgrade head

python3 app/


