from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variavle(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is required but not set.")
    return value

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ENV = os.getenv("ENV", "development")