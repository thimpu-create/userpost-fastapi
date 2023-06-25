from pydantic import BaseModel

class UserSchema(BaseModel):
    username : str
    password : str

    class config :
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class PostSchema(BaseModel):
    title : str | None = None

    class config:
        orm_mode = True