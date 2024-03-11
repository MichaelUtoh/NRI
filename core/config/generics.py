from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field
from zxcvbn import zxcvbn

from .database import PyObjectId


class GenericModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = datetime.now()


def pwd_strength_checker(data):
    res = zxcvbn(data.password)
    if not res["score"] >= 3:
        return False
    return True
