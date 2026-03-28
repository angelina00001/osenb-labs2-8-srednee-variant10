"""Кастомные исключения"""
from fastapi import HTTPException
from typing import Optional


class AppException(HTTPException):
    """Базовое исключение приложения"""
    def __init__(
        self,
        status_code: int = 400,
        detail: str = "Произошла ошибка",
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ValidationError(AppException):
    """Ошибка валидации"""
    def __init__(self, detail: str = "Ошибка валидации данных"):
        super().__init__(status_code=422, detail=detail)


class NotFoundError(AppException):
    """Ресурс не найден"""
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(status_code=404, detail=detail)


class ServiceError(AppException):
    """Ошибка в сервисе"""
    def __init__(self, detail: str = "Внутренняя ошибка сервиса"):
        super().__init__(status_code=500, detail=detail)
