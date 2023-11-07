from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    organizer: bool = False


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class EventLocation(BaseModel):
    cep: int
    number: int
    street: str
    complement: str | None


class EventSchema(BaseModel):
    name: str
    age: int
    description: str
    location: EventLocation
    organizer: int   # user_id


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
