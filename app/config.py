import os

class Config:
    DEBUG: bool = bool(os.getenv('DEBUG', False))
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = os.getenv('PORT', 8000)
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'transactions_db')
    DB_URI: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    ALEMBIC_DB_URI: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


class TestConfig(Config):
    DB_USER = os.getenv('TEST_DB_USER', 'admin')
    DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('TEST_DB_HOST', 'localhost')
    DB_NAME = os.getenv('TEST_DB_NAME', 'test_transactions_db')
    DB_URI: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
