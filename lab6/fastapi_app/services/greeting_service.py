from models.schemas import GreetingRequest, GreetingResponse
from datetime import datetime
from typing import Dict


class GreetingService:
    def __init__(self):
        self.greetings: Dict[str, Dict[str, str]] = {
            "ru": {
                "formal": "Здравствуйте, {name}!",
                "informal": "Привет, {name}!",
                "morning": "Доброе утро, {name}!",
                "day": "Добрый день, {name}!",
                "evening": "Добрый вечер, {name}!",
                "night": "Доброй ночи, {name}!"
            },
            "en": {
                "formal": "Hello, {name}!",
                "informal": "Hi, {name}!",
                "morning": "Good morning, {name}!",
                "day": "Good afternoon, {name}!",
                "evening": "Good evening, {name}!",
                "night": "Good night, {name}!"
            }
        }
    
    def get_greeting(self, request: GreetingRequest) -> GreetingResponse:
        name = request.name.strip()
        if not name:
            name = "Гость"

        lang = request.language if request.language in self.greetings else "ru"

        hour = datetime.now().hour
        
        if hour < 6:
            greeting_type = "night"
        elif hour < 12:
            greeting_type = "morning"
        elif hour < 18:
            greeting_type = "day"
        else:
            greeting_type = "evening"

        greeting_template = self.greetings[lang][greeting_type]
        message = greeting_template.format(name=name)

        return GreetingResponse(
            success=True,
            message=message,
            timestamp=datetime.now(),
            data={
                "original_name": request.name,
                "greeting_type": greeting_type,
                "language": lang
            }
        )
    
    def get_available_languages(self) -> list:
        return list(self.greetings.keys())
    
    def get_available_greeting_types(self, language: str = "ru") -> list:
        lang = language if language in self.greetings else "ru"
        return list(self.greetings[lang].keys())
