from aiohttp.web import Request
from marshmallow import Schema, fields, ValidationError
from models import User

class UserSchema(Schema):
    name = fields.String(required=True)

    async def load_from_request(self, requset: Request):
        try:
            data = await requset.json()
        except Exception:
            data = {}

        return self.load(data)


TransactionSerializer = UserSchema()