from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True)

    def full_name(self) -> str:
        return self.id

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]
