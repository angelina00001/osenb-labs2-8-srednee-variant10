"""Сервис бизнес-логики для приветствий"""
from datetime import datetime
from typing import Dict
from models.schemas import GreetingRequest, GreetingResponse
from core.exceptions import ValidationError
from config.settings import settings


class GreetingService:
    """Сервис для работы с приветствиями"""
    
    def __init__(self):
        self._start_time = datetime.now()
        
        # База данных приветствий
        self._greetings_db: Dict[str, Dict[str, str]] = {
            "ru": {
                "formal": "Здравствуйте, {name}!",
                "neutral": "Привет, {name}!",
                "happy": "Приветствую, {name}! Рад вас видеть!",
                "morning": "Доброе утро, {name}!",
                "day": "Добрый день, {name}!",
                "evening": "Добрый вечер, {name}!",
                "night": "Доброй ночи, {name}!"
            },
            "en": {
                "formal": "Hello, {name}!",
                "neutral": "Hi, {name}!",
                "happy": "Welcome, {name}! Great to see you!",
                "morning": "Good morning, {name}!",
                "day": "Good afternoon, {name}!",
                "evening": "Good evening, {name}!",
                "night": "Good night, {name}!"
            },
            "es": {
                "formal": "¡Hola, {name}!",
                "neutral": "¡Hola, {name}!",
                "happy": "¡Bienvenido, {name}! ¡Me alegra verte!",
                "morning": "¡Buenos días, {name}!",
                "day": "¡Buenas tardes, {name}!",
                "evening": "¡Buenas tardes, {name}!",
                "night": "¡Buenas noches, {name}!"
            },
            "fr": {
                "formal": "Bonjour, {name}!",
                "neutral": "Salut, {name}!",
                "happy": "Bienvenue, {name}! Ravi de vous voir!",
                "morning": "Bonjour, {name}!",
                "day": "Bon après-midi, {name}!",
                "evening": "Bonsoir, {name}!",
                "night": "Bonne nuit, {name}!"
            }
        }
        
        # Доступные настройки
        self._available_moods = ["formal", "neutral", "happy"]
    
    def get_uptime(self) -> float:
        """Получить время работы сервиса в секундах"""
        return (datetime.now() - self._start_time).total_seconds()
    
    def validate_request(self, request: GreetingRequest) -> None:
        """Валидация запроса"""
        # Проверка языка
        if request.language not in settings.SUPPORTED_LANGUAGES:
            raise ValidationError(
                f"Неподдерживаемый язык. Доступные: {settings.SUPPORTED_LANGUAGES}"
            )
        
        # Проверка настроения
        if request.mood not in self._available_moods:
            raise ValidationError(
                f"Неподдерживаемое настроение. Доступные: {self._available_moods}"
            )
    
    def get_time_based_greeting(self, language: str) -> str:
        """Получить приветствие на основе времени суток"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "day"
        elif 18 <= hour < 23:
            return "evening"
        else:
            return "night"
    
    def generate_greeting(self, request: GreetingRequest) -> GreetingResponse:
        """
        Генерация приветственного сообщения
        """
        try:
            # Валидация
            self.validate_request(request)
            
            # Обработка имени
            name = request.name.strip()
            if not name:
                name = settings.DEFAULT_NAME
            
            # Получение приветствия
            language = request.language
            mood = request.mood
            
            # Для нейтрального настроения используем приветствие по времени суток
            if mood == "neutral":
                time_greeting = self.get_time_based_greeting(language)
                greeting_template = self._greetings_db[language][time_greeting]
                used_mood = time_greeting
            else:
                greeting_template = self._greetings_db[language][mood]
                used_mood = mood
            
            # Форматирование сообщения
            message = greeting_template.format(name=name)
            
            # Формирование ответа
            return GreetingResponse(
                success=True,
                message=message,
                timestamp=datetime.now(),
                request_data={
                    "original_name": request.name,
                    "processed_name": name,
                    "language": language,
                    "mood": used_mood
                },
                metadata={
                    "greeting_type": used_mood,
                    "time_of_day": self.get_time_based_greeting(language),
                    "supported_languages": settings.SUPPORTED_LANGUAGES
                }
            )
            
        except ValidationError:
            raise
        except Exception as e:
            from core.exceptions import ServiceError
            raise ServiceError(f"Ошибка генерации приветствия: {str(e)}")
    
    def get_service_info(self) -> dict:
        """Получить информацию о сервисе"""
        return {
            "name": "Greeting Service",
            "supported_languages": settings.SUPPORTED_LANGUAGES,
            "available_moods": self._available_moods,
            "uptime_seconds": self.get_uptime(),
            "greeting_count": len(self._greetings_db)
        }


# Создаем экземпляр сервиса
greeting_service = GreetingService()
