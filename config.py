"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Render uses postgres://, SQLAlchemy 1.4+ requires postgresql://
    _db_url = os.getenv("DATABASE_URL", "sqlite:///tasks.db")
    SQLALCHEMY_DATABASE_URI = (
        _db_url.replace("postgres://", "postgresql://", 1)
        if _db_url.startswith("postgres://")
        else _db_url
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Smorest / OpenAPI
    API_TITLE = os.getenv("API_TITLE", "Tasks Manager API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
