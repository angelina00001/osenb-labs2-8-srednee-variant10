"""Конфигурация приложения"""

class Settings:
    """Настройки приложения"""
    APP_NAME: str = "FastAPI Parameter App"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    DEFAULT_NAME: str = "Гость"
    SUPPORTED_LANGUAGES: list = ["ru", "en", "es", "fr"]
    
    # Настройки API
    API_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    
    class Config:
        env_file = ".env"


settings = Settings()
