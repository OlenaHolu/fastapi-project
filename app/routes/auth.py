from fastapi import APIRouter
from app.controllers import auth_controller

router = APIRouter()

router.post("/register")(auth_controller.register)
router.post("/login")(auth_controller.login)
router.get("/auth/google")(auth_controller.redirect_to_google)
router.post("/auth/google/callback")(auth_controller.handle_google_callback)
