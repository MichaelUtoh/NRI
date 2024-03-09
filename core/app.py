from fastapi import FastAPI

from .routers import food


app = FastAPI(
    title="Agba Cook",
    summary="Simple FastAPI ReST API, MongoDB collection.",
)
app.include_router(food.router)
