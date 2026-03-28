"""Маршруты API"""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from datetime import datetime

from models.schemas import (
    GreetingRequest, 
    GreetingResponse, 
    HealthResponse,
    ErrorResponse
)
from services.greeting import greeting_service
from api.dependencies import verify_api_key, require_name, validate_language
from config.settings import settings
from core.exceptions import AppException


# Создаем роутер
router = APIRouter(
    prefix=settings.API_PREFIX,
    tags=["greetings"],
    dependencies=[Depends(verify_api_key)]  # Применяем ко всем маршрутам
)


@router.get("/", summary="Информация о API")
async def api_info():
    """
    Получить информацию о доступных эндпоинтах API
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "endpoints": {
            "health": f"{settings.API_PREFIX}/health",
            "greet_get": f"{settings.API_PREFIX}/greet",
            "greet_post": f"{settings.API_PREFIX}/greet",
            "service_info": f"{settings.API_PREFIX}/service/info",
            "docs": settings.DOCS_URL
        },
        "description": "API для генерации персонализированных приветствий"
    }


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Проверка здоровья приложения"
)
async def health_check():
    """
    Проверка работоспособности приложения
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        timestamp=datetime.now(),
        uptime=greeting_service.get_uptime()
    )


@router.get(
    "/greet",
    response_model=GreetingResponse,
    summary="Получить приветствие (GET)"
)
async def greet_via_get(
    name: str = Query(
        settings.DEFAULT_NAME,
        description="Имя для приветствия",
        min_length=1,
        max_length=50
    ),
    language: str = Query(
        "ru",
        description=f"Язык приветствия. Доступные: {settings.SUPPORTED_LANGUAGES}"
    ),
    mood: str = Query(
        "neutral",
        description="Настроение приветствия (formal/neutral/happy)"
    )
):
    """
    Получить персонализированное приветствие через GET запрос
    
    - **name**: Имя пользователя
    - **language**: Язык приветствия
    - **mood**: Настроение приветствия
    """
    try:
        # Валидация и обработка параметров
        validated_name = require_name(name)
        validated_language = validate_language(language)
        
        # Создаем запрос
        request = GreetingRequest(
            name=validated_name,
            language=validated_language,
            mood=mood
        )
        
        # Генерируем приветствие
        return greeting_service.generate_greeting(request)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/greet",
    response_model=GreetingResponse,
    summary="Получить приветствие (POST)"
)
async def greet_via_post(request: GreetingRequest):
    """
    Получить персонализированное приветствие через POST запрос
    
    - **name**: Имя пользователя (обязательно)
    - **language**: Язык приветствия
    - **mood**: Настроение приветствия
    """
    try:
        return greeting_service.generate_greeting(request)
    except AppException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get(
    "/greet/{name}",
    response_model=GreetingResponse,
    summary="Получить приветствие по пути (path parameter)"
)
async def greet_via_path(
    name: str,
    language: Optional[str] = Query("ru", description="Язык приветствия"),
    mood: Optional[str] = Query("neutral", description="Настроение приветствия")
):
    """
    Получить приветствие с именем в пути URL
    
    - **name**: Имя пользователя (в пути URL)
    - **language**: Язык приветствия
    - **mood**: Настроение приветствия
    """
    try:
        request = GreetingRequest(
            name=name,
            language=language,
            mood=mood
        )
        return greeting_service.generate_greeting(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/service/info", summary="Информация о сервисе приветствий")
async def service_info():
    """
    Получить техническую информацию о сервисе
    """
    return {
        "success": True,
        "data": greeting_service.get_service_info(),
        "timestamp": datetime.now()
    }


@router.get("/languages", summary="Поддерживаемые языки")
async def supported_languages():
    """
    Получить список поддерживаемых языков
    """
    return {
        "success": True,
        "languages": settings.SUPPORTED_LANGUAGES,
        "default_language": "ru",
        "count": len(settings.SUPPORTED_LANGUAGES)
    }


@router.get("/moods", summary="Доступные настроения")
async def available_moods():
    """
    Получить список доступных настроений для приветствий
    """
    return {
        "success": True,
        "moods": greeting_service._available_moods,
        "default_mood": "neutral"
    }


# Обработчик ошибок (можно добавить в middleware)
@router.get("/error-test", include_in_schema=False)
async def error_test():
    """
    Тестовый эндпоинт для проверки обработки ошибок
    """
    raise HTTPException(
        status_code=400,
        detail="Это тестовая ошибка для демонстрации"
    )
