from typing import Optional

from fastapi import FastAPI, HTTPException, status
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()


# ---------- Request / Response bodies ----------
class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None


# (Authentication removed — routes are public)


# ---------- GET with query params ----------
@app.get("/users")
def list_users():
    return {
        "success": True,
        "message": "Users fetched successfully",
        "data": [],
    }


# ---------- GET by path param + headers/auth ----------
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User fetched successfully",
        "data": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
        },
    }


# ---------- POST with request body ----------
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    created_user = UserOut(
        id=1,
        name=user.name,
        email=user.email,
        age=user.age,
    )

    return {
        "success": True,
        "message": "User created successfully",
        "data": created_user,
    }


# ---------- PUT: replace full object ----------
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User fully updated",
        "data": {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
        },
    }


# ---------- PATCH: partial update ----------
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserPatch):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")

    current_user = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
    }

    update_data = user.model_dump(exclude_unset=True)
    current_user.update(update_data)

    return {
        "success": True,
        "message": "User partially updated",
        "data": current_user,
    }


# ---------- DELETE ----------
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User deleted successfully",
        "data": None,
    }


# ---------- Lambda entrypoint ----------
handler = Mangum(app)