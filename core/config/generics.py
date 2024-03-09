from typing import Optional

from datetime import datetime

from pydantic import BaseModel, Field

from .database import PyObjectId


class GenericModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = datetime.now()
