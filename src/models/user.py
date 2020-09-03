from src.models.base import Base, pydantic_model_creator, fields


class User(Base):
    '''
    User model
    '''
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    display_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128, null=True)

    def full_name(self) -> str:
        if self.display_name:
            return self.display_name
        return self.username

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(
    User,
    name="UserIn",
    exclude_readonly=True)
