from bson import ObjectId

from fastapi import APIRouter, Body, HTTPException, Response, status
from pymongo import ReturnDocument

from ..models.foods import FoodCollection, FoodModel, UpdateFoodModel
from ..config.database import food_collection

router = APIRouter()


@router.post(
    "/foods/",
    response_description="Add new food item",
    response_model=FoodModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_food(food: FoodModel = Body(...)):
    new_food = await food_collection.insert_one(
        food.model_dump(by_alias=True, exclude=["id"])
    )
    created_food = await food_collection.find_one({"_id": new_food.inserted_id})
    return created_food


@router.get(
    "/foods/",
    response_description="List all foods",
    response_model=FoodCollection,
    response_model_by_alias=False,
)
async def list_food():
    return FoodCollection(foods=await food_collection.find().to_list(1000))


@router.get(
    "/foods/{id}",
    response_description="Get a single food item",
    response_model=FoodModel,
    response_model_by_alias=False,
)
async def show_food(id: str):
    """
    Get the record for a specific food, looked up by `id`.
    """
    if (food := await food_collection.find_one({"_id": ObjectId(id)})) is not None:
        return food

    raise HTTPException(status_code=404, detail=f"food {id} not found")


@router.put(
    "/foods/{id}",
    response_description="Update a food",
    response_model=FoodModel,
    response_model_by_alias=False,
)
async def update_food(id: str, food: UpdateFoodModel = Body(...)):
    """
    Update individual fields of an existing food record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    food = {k: v for k, v in food.model_dump(by_alias=True).items() if v is not None}

    if len(food) >= 1:
        update_result = await food_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": food},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"food {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_food := await food_collection.find_one({"_id": id})) is not None:
        return existing_food

    raise HTTPException(status_code=404, detail=f"food {id} not found")


@router.delete("/foods/{id}", response_description="Delete a food item")
async def delete_food(id: str):
    """
    Remove a single food record from the database.
    """
    delete_result = await food_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"food {id} not found")
