from bson import ObjectId

import bcrypt
from fastapi import APIRouter, Body, HTTPException, Response, status
from pymongo import ReturnDocument

from ..models.accounts import UserCollection, UserModel, UpdateUserModel
from ..schemas.accounts import RegisterSerializer
from ..config.auth import AuthHandler
from ..config.database import user_collection
from ..config.generics import pwd_strength_checker

auth_handler = AuthHandler()
router = APIRouter(prefix="/auth/accounts", tags=["Authentication"])


@router.post(
    "/register/",
    response_description="Add new user",
    response_model=RegisterSerializer,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def register(user: UserModel = Body(...)):
    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    if not pwd_strength_checker(user):
        raise HTTPException(status_code=400, detail="Password is not strong enough!")

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    data = {"email": user.email.lower(), "password": hashed_pwd}
    new_user = await user_collection.insert_one(data)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})

    payload = {
        "email": created_user["email"],
        "access_token": auth_handler.encode_token(user.email),
        "refresh_token": auth_handler.encode_refresh_token(user.email),
    }
    return payload


@router.get(
    "/users/all/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_user():
    return UserCollection(users=await user_collection.find().to_list(1000))


@router.get(
    "/users/{id}",
    response_description="Get a single user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (user := await user_collection.find_one({"_id": ObjectId(id)})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.put(
    "/users/{id}",
    response_description="Update a user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    """
    Update individual fields of an existing user record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    user = {k: v for k, v in user.model_dump(by_alias=True).items() if v is not None}

    if len(user) >= 1:
        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"user {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := await user_collection.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@router.delete("/users/{id}", response_description="Delete a user item")
async def delete_user(id: str):
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"user {id} not found")
