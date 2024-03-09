from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from ..config.generics import GenericModel


class FoodModel(GenericModel):
    name: str = Field(...)
    description: str = Field(...)
    amount_per_scoop: float = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Basmati Rice",
                "description": "Long grain foreign rice from Asia",
                "amount_per_scoop": 1550.21,
            }
        },
    )


class UpdateFoodModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount_per_scoop: Optional[float] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Basmati Rice",
                "description": "Long grain foreign rice from Asia",
                "amount_per_scoop": 1550.21,
            }
        },
    )


class FoodCollection(BaseModel):
    foods: List[FoodModel]
