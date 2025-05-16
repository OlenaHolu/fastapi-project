from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.schemas.user_schema import UpdateUserRequest
from app.controllers import user_controller
from app.database.connection import SessionLocal
from app.models.user import User
from app.models.post import Post
from app.core.errors import error
import os, requests

router = APIRouter()

@router.get("/user")
def me(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == current_user["id"]).first()
        if not user:
            return error(1503, "User not found", 404)
        
        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "photo": user.photo
            }
        }
    finally:
        db.close()


@router.put("/logout")
def logout():
    return {"message": "Logout successful"}

@router.patch("/user/update")
def update_user(data: UpdateUserRequest, current_user: dict = Depends(get_current_user)):
    return user_controller.update_profile(data, current_user["id"])

@router.delete("/user/delete")
def delete_user(current_user: dict = Depends(get_current_user)):
    return user_controller.delete_user(current_user["id"])
