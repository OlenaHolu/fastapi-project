from fastapi import HTTPException
from app.schemas.auth_schema import LoginRequest
from app.schemas.auth_schema import RegisterRequest
from sqlalchemy.exc import IntegrityError
from app.core.errors import error
from app.database.connection import SessionLocal
from app.models.user import User
from app.dependencies.auth import create_access_token
import hashlib
from app.core.security import hash_password
from app.core.security import verify_password

def register(data: RegisterRequest):
    db = SessionLocal()
    try:
        hashed_pw = hash_password(data.password)

        user = User(
            name=data.name,
            email=data.email,
            password=hashed_pw,
            photo=None
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    except IntegrityError:
        db.rollback()
        return error(1203, "Email already exists", 409)
    
    except Exception as e:
        db.rollback()
        return error(1000, "Internal server error", 500)
    
    finally:
        db.close()

def login(data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not verify_password(data.password, user.password):
            return error(1503, "Invalid credentials", 401)
        
        token = create_access_token({"sub": str(user.id)})

        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },
            "token": token
        }
    
    finally:
        db.close()

def redirect_to_google():
    return {"message": "Redirecting to Google"}

def handle_google_callback():
    return {"message": "Handling Google callback"}