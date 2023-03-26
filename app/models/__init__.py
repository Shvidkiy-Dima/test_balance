from datetime import datetime
import enum
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, INTEGER, ForeignKey, DECIMAL, Integer, select, UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True)
    balance = Column(DECIMAL(12, 2), default=Decimal(0.00), nullable=False)
    name = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    async def get_locked(cls, user_id, session):
        """
        UPDATE FOR NOWAIT - lock row from account table while transaction not end.
        :return: (Account, is_locked)
        """
        try:
            usr = (await session.execute(select(User).where(User.id==user_id).with_for_update(nowait=True))).scalar()
        except Exception:
            return None, True

        return usr, False


class Transaction(Base):
    __tablename__ = 'transaction'

    class TransactionType(enum.Enum):
        DEPOSIT = 'DEPOSIT'
        WITHDRAW = 'WITHDRAW'

    amount = Column(DECIMAL(12, 2), nullable=False)
    transaction_type = Column(String, nullable=False)
    uid = Column(UUID, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
