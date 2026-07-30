from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
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


# ---------- Fake auth ----------
def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.replace("Bearer ", "")
    if token != "my-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return token


# ---------- GET with query params ----------
@app.get("/users")
def list_users(
    search: Optional[str] = Query(None, description="Search by name"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return {
        "success": True,
        "message": "Users fetched successfully",
        "data": [],
        "filters": {
            "search": search,
            "page": page,
            "limit": limit,
        },
    }


# ---------- GET by path param + headers/auth ----------
@app.get("/users/{user_id}")
def get_user(user_id: int, token: str = Depends(verify_token)):
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
def create_user(user: UserCreate, token: str = Depends(verify_token)):
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
def update_user(user_id: int, user: UserCreate, token: str = Depends(verify_token)):
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
def patch_user(user_id: int, user: UserPatch, token: str = Depends(verify_token)):
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
def delete_user(user_id: int, token: str = Depends(verify_token)):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "success": True,
        "message": "User deleted successfully",
        "data": None,
    }


# ---------- Lambda entrypoint ----------
handler = Mangum(app)