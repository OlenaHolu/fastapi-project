from fastapi import HTTPException
from app.database.connection import SessionLocal
from app.models.user import User
from app.core.errors import error
from app.schemas.user_schema import UpdateUserRequest
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

def update_profile(data: UpdateUserRequest, current_user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == current_user_id).first()
        if not user:
            return error(1501, "User not registered", 401)
        
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            exists = db.query(User).filter(User.email == data.email, User.id !=current_user_id).first()
            if exists:
                return error(1203, "Email already exists", 422)
            user.email = data.email
        
        if data.photo is not None:
            user.photo = data.photo
        
        if data.password is not None:
            user.password = hash_password(data.password)
            
        db.commit()
        db.refresh(user)

        return {
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "photo": user.photo
            }
        }
    
    except Exception as e:
        db.rollback()
        return error(1000, "Failed to update profile", 500)
    
    finally:
        db.close()

def delete_user(current_user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == current_user_id).first()
        if not user:
            return error(1501, "User not registered", 401)
        
        # Delete avatar from Supebase if not is from Google
        if user.photo and "google" not in user.photo:
            avatar_filename = os.path.basename(user.photo)
            headers = {
                "apikey": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
                "Authorization": f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}",
            }

            r = request.delete(
                f"{os.getenv('SUPABASE_URL')}/storage/v1/object/{os.getenv('SUPABASE_BUCKET_AVATARS')}/{avatar_filename}",
                headers=headers
            )
            if r.status_code >= 400:
                return error(1000, "Failed to delete avatar from Supabase", 500)
            
        posts = db.query(Post).filter(Post.user_id == current_user_id).all()
        for post in posts:
            if post.image_path:
                image_filename = post.image_path
                headers = {
                    "apikey": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
                    "Authorization": f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}",
                }
                r = request.delete(
                    f"{os.getenv('SUPABASE_URL')}/storage/v1/object/{os.getenv('SUPABASE_BUCKET_POSTS')}/{image_filename}",
                    headers=headers
                )
                if r.status_code >= 400:
                    return error(1000, f"Failed to delete post image from Supabase: {image_filename}", 500)
            db.delete(post)

        db.delete(user)
        db.commit()

        return {"message": "User and all associated content deleted successfully"}
    
    except Exception as e:
        db.rollback()
        return error(1000, "Failed to delete user", 500)
    
    finally:
        db.close()
