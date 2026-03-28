"""Pydantic схемы для валидации данных"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GreetingRequest(BaseModel):
    """Схема запроса приветствия"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Имя пользователя",
        example="Иван"
    )
    language: Optional[str] = Field(
        "ru",
        description="Язык приветствия (ru/en/es/fr)",
        example="ru"
    )
    mood: Optional[str] = Field(
        "neutral",
        description="Настроение (happy/neutral/formal)",
        example="neutral"
    )


class GreetingResponse(BaseModel):
    """Схема ответа с приветствием"""
    success: bool
    message: str
    timestamp: datetime
    request_data: dict
    metadata: dict = {}


class HealthResponse(BaseModel):
    """Схема проверки здоровья"""
    status: str
    app_name: str
    version: str
    timestamp: datetime
    uptime: Optional[float] = None


class ErrorResponse(BaseModel):
    """Схема ошибки"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
