#!/bin/sh

python /app/check_conn.py --service-name test_db --port 5432  --ip test_db


pytest tests/


