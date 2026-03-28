from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GreetingRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    language: Optional[str] = Field("ru", description="Язык приветствия (ru/en)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван",
                "language": "ru"
            }
        }


class GreetingResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime
    data: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Привет, Иван!",
                "timestamp": "2023-11-15T10:30:00",
                "data": {
                    "original_name": "Иван",
                    "greeting_type": "informal",
                    "language": "ru"
                }
            }
        }


class HealthCheck(BaseModel):
    status: str
    app_name: str
    version: str
    timestamp: datetime
