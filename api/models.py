import re
import uuid
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ShowUser(TunedModel):
    users_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str = Field(..., description="Name of the user")
    surname: str = Field(..., description="Surname of the user")
    email: EmailStr


@field_validator("name")
def validate_name(cls,value):
    if not LETTER_MATCH_PATTERN.match(value):
        raise HTTPException(status_code=422,detail="Name should contains only letters")
    return value
@field_validator("surname")
def validate_surname(cls,value):
    if not LETTER_MATCH_PATTERN.match(value):
        raise HTTPException(status_code=422, detail="Surname should contains only letters")
    return value