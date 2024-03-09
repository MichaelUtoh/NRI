import motor.motor_asyncio
from decouple import config
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated


client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"))
db = client.zen_db

food_collection = db.get_collection("food")
user_collection = db.get_collection("accounts")

PyObjectId = Annotated[str, BeforeValidator(str)]
