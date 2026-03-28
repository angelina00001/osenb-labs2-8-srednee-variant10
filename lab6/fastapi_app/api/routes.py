from fastapi import APIRouter, HTTPException
from models.schemas import GreetingRequest, GreetingResponse, HealthCheck
from services.greeting_service import GreetingService
from datetime import datetime

router = APIRouter(
    prefix="/api/v1",
    tags=["greetings"]
)

greeting_service = GreetingService()


@router.get("/", summary="Корневой эндпоинт")
async def root():
    return {
        "message": "Добро пожаловать в FastAPI Hello App!",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "greet": "/api/v1/greet",
            "languages": "/api/v1/languages",
            "docs": "/docs"
        }
    }


@router.get("/health", response_model=HealthCheck, summary="Проверка здоровья")
async def health_check():
    return HealthCheck(
        status="ok",
        app_name="FastAPI Hello App",
        version="1.0.0",
        timestamp=datetime.now()
    )


@router.post("/greet", response_model=GreetingResponse, summary="Получить приветствие")
async def greet(request: GreetingRequest):
    try:
        return greeting_service.get_greeting(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/greet", response_model=GreetingResponse, summary="Получить приветствие (GET)")
async def greet_get(name: str = "Гость", language: str = "ru"):
    try:
        request = GreetingRequest(name=name, language=language)
        return greeting_service.get_greeting(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages", summary="Получить доступные языки")
async def get_languages():
    return {
        "success": True,
        "languages": greeting_service.get_available_languages(),
        "description": "Доступные языки для приветствий"
    }


@router.get("/greeting-types", summary="Получить типы приветствий")
async def get_greeting_types(language: str = "ru"):
    try:
        types = greeting_service.get_available_greeting_types(language)
        return {
            "success": True,
            "language": language,
            "greeting_types": types
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
