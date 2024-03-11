from pydantic import BaseModel, EmailStr


class RegisterSerializer(BaseModel):
    email: EmailStr
    access_token: str
    refresh_token: str
