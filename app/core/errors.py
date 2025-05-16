from fastapi import HTTPException

def error(code: int, message: str, status_code: int = 400):
    raise HTTPException(
        status_code=status_code,
        detail={
            "errorCode": code,
            "message": message
        }
    )

# 🔁 General (1000–1099)
def internal_error():
    return error(1000, "Internal server error", 500)

def unknown_error():
    return error(1001, "Unknown error", 500)

# 🔐 Auth / Tokens (1100–1199)
def token_missing():
    return error(1101, "Token not provided", 401)

def token_expired():
    return error(1102, "Token expired", 401)

def unauthorized():
    return error(1103, "Unauthorized", 401)

# 📝 Validation (1200–1299)
def email_required():
    return error(1201, "Email is required", 422)

def password_too_short():
    return error(1202, "Password too short", 422)

def email_exists():
    return error(1203, "Email already exists", 409)

# 📝 Post/Feed Errors (1300–1399)
def post_save_failed():
    return error(1300, "Failed to save post", 500)

# 🧑 User (1500–1599)
def user_not_registered():
    return error(1501, "User not registered", 404)

def incomplete_data():
    return error(1502, "Incomplete data", 422)

def invalid_credentials():
    return error(1503, "Invalid credentials", 401)

# 🔗 Google Login (1400+ si lo usas)
def google_code_missing():
    return error(1401, "Missing Google authorization code", 400)

def google_login_failed():
    return error(1500, "Google login failed", 500)
