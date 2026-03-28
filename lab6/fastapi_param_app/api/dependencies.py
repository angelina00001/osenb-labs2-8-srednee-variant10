"""Зависимости для API"""
from typing import Optional
from fastapi import Header, HTTPException
from services.greeting import greeting_service
from config.settings import settings


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, description="API ключ")
) -> Optional[str]:
    """
    Простая проверка API ключа.
    В реальном приложении здесь была бы полноценная аутентификация.
    """
    if not x_api_key:
        # Разрешаем запросы без ключа для демо
        return None
    
    # Простая проверка для демо (в реальном приложении проверяем в БД)
    if x_api_key.startswith("demo_"):
        return x_api_key
    
    raise HTTPException(
        status_code=401,
        detail="Неверный API ключ. Используйте 'demo_key' для тестирования."
    )


async def get_greeting_service():
    """Получить сервис приветствий"""
    return greeting_service


# Простые зависимости для проверки
def require_name(name: str) -> str:
    """Проверка наличия имени"""
    if not name or not name.strip():
        name = settings.DEFAULT_NAME
    return name.strip()


def validate_language(language: str) -> str:
    """Валидация языка"""
    if language not in settings.SUPPORTED_LANGUAGES:
        return "ru"  # Значение по умолчанию
    return language
