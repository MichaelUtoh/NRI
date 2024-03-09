from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator

from ..config.generics import GenericModel


class UserModel(GenericModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    title: Optional[str] = Field()
    address: str = Field()
    favorites: Optional[List] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "sample": {
                "email": "zinny21@gmail.com",
                "password": "pass1234",
                "first_name": "Ezinne",
                "last_name": "Sumbodi",
                "title": "Mrs",
                "address": "21, Fadahunsi Avenue",
            }
        },
    )

    @validator("first_name")
    def validate_first_name(cls, value):
        if value and len(value) < 2:
            raise ValueError("First name must be at least 2 characters long")
        return value


class UpdateUserModel(GenericModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    address: Optional[str] = None
    favorites: Optional[List] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "sample": {
                "email": "zinny21@gmail.com",
                "password": "pass1234",
                "first_name": "Ezinne",
                "last_name": "Sumbodi",
                "title": "Mrs",
                "address": "21, Fadahunsi Avenue",
            }
        },
    )


class UserCollection(BaseModel):
    foods: List[UserModel]
