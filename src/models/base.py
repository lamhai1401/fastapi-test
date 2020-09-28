from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


class Base(models.Model):
    '''
    Base model for all table
    '''
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Config:
        ignore_extra = True
        # allow_population_by_alias = True


class Response(BaseModel):
    message: str
