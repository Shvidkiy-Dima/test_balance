from aiohttp.web import Request
from marshmallow import Schema,  fields, ValidationError
from marshmallow.validate import OneOf

from models import User, Transaction

class TransactionSchema(Schema):
    user_id = fields.Number(required=True)
    uid = fields.UUID(required=True)
    transaction_type = fields.String(required=True,
                                     data_key='type',
                                     validate=OneOf([Transaction.TransactionType.WITHDRAW.value,
                                                        Transaction.TransactionType.DEPOSIT.value]))
    amount = fields.Decimal(required=True)
    timestamp = fields.DateTime()


    def dump(self, *args, **kwargs):
        res = super().dump(*args, **kwargs)
        res['amount'] = str(res['amount'])
        return res


TransactionSerializer = TransactionSchema()