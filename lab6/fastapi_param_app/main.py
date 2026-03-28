import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.settings import settings
from api.endpoints import router
from core.exceptions import AppException
from models.schemas import ErrorResponse


def create_application() -> FastAPI:
    """
    Фабрика для создания приложения FastAPI
    """
    # Инициализация приложения
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Простое FastAPI приложение с модульной архитектурой",
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        debug=settings.DEBUG
    )
    
    # Настройка CORS (Cross-Origin Resource Sharing)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене заменить на конкретные домены
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Middleware для измерения времени ответа
    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Регистрация маршрутов
    application.include_router(router)
    
    # Обработчики ошибок
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error="Ошибка валидации",
                detail=str(exc),
                timestamp=time.time()
            ).dict()
        )
    
    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="HTTP ошибка",
                detail=exc.detail,
                timestamp=time.time()
            ).dict()
        )
    
    @application.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="Ошибка приложения",
                detail=exc.detail,
                timestamp=time.time()
            ).dict()
        )
    
    @application.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Внутренняя ошибка сервера",
                detail=str(exc),
                timestamp=time.time()
            ).dict()
        )
    
    # Корневой маршрут с HTML интерфейсом
    @application.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def root():
        return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>FastAPI Параметр Приложение</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                
                header {
                    text-align: center;
                    color: white;
                    padding: 40px 0;
                }
                
                header h1 {
                    font-size: 3em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                
                header p {
                    font-size: 1.2em;
                    opacity: 0.9;
                }
                
                .content {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 30px;
                    margin-bottom: 40px;
                }
                
                @media (max-width: 768px) {
                    .content {
                        grid-template-columns: 1fr;
                    }
                }
                
                .card {
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                
                .card h2 {
                    color: #333;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }
                
                .form-group {
                    margin-bottom: 20px;
                }
                
                label {
                    display: block;
                    margin-bottom: 8px;
                    color: #555;
                    font-weight: 600;
                }
                
                input, select {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s;
                }
                
                input:focus, select:focus {
                    outline: none;
                    border-color: #667eea;
                }
                
                .button-group {
                    display: flex;
                    gap: 10px;
                    margin-top: 20px;
                }
                
                button {
                    flex: 1;
                    padding: 14px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                .btn-get {
                    background: #4CAF50;
                    color: white;
                }
                
                .btn-get:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                
                .btn-post {
                    background: #2196F3;
                    color: white;
                }
                
                .btn-post:hover {
                    background: #0b7dda;
                    transform: translateY(-2px);
                }
                
                .btn-path {
                    background: #9C27B0;
                    color: white;
                }
                
                .btn-path:hover {
                    background: #7B1FA2;
                    transform: translateY(-2px);
                }
                
                .result {
                    margin-top: 30px;
                    padding: 25px;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    border-radius: 10px;
                    color: white;
                    display: none;
                }
                
                .result.show {
                    display: block;
                    animation: fadeIn 0.5s;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                .result h3 {
                    margin-bottom: 15px;
                    font-size: 1.4em;
                }
                
                .result .message {
                    font-size: 1.8em;
                    font-weight: bold;
                    margin: 15px 0;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
                }
                
                .result .details {
                    font-size: 0.9em;
                    opacity: 0.9;
                    margin-top: 15px;
                }
                
                .api-info {
                    margin-top: 20px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    font-size: 14px;
                }
                
                .api-info h4 {
                    color: #333;
                    margin-bottom: 10px;
                }
                
                .api-info code {
                    background: #e9ecef;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    color: #d63384;
                }
                
                footer {
                    text-align: center;
                    color: white;
                    padding: 20px;
                    margin-top: 40px;
                    opacity: 0.8;
                }
                
                .endpoints-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                
                .endpoint-card {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }
                
                .endpoint-card h4 {
                    color: #333;
                    margin-bottom: 10px;
                }
                
                .endpoint-card p {
                    color: #666;
                    font-size: 0.9em;
                }
                
                .badge {
                    display: inline-block;
                    padding: 4px 8px;
                    background: #667eea;
                    color: white;
                    border-radius: 4px;
                    font-size: 0.8em;
                    margin-right: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1> FastAPI Параметр Приложение</h1>
                    <p>Модульное приложение с разделением слоев</p>
                </header>
                
                <div class="content">
                    <div class="card">
                        <h2> Тестовая форма</h2>
                        
                        <div class="form-group">
                            <label for="name">Ваше имя:</label>
                            <input type="text" id="name" placeholder="Введите ваше имя" value="Алексей">
                        </div>
                        
                        <div class="form-group">
                            <label for="language">Язык приветствия:</label>
                            <select id="language">
                                <option value="ru">🇷🇺 Русский</option>
                                <option value="en">🇬🇧 English</option>
                                <option value="es">🇪🇸 Español</option>
                                <option value="fr">🇫🇷 Français</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="mood">Настроение:</label>
                            <select id="mood">
                                <option value="formal">Формальное</option>
                                <option value="neutral" selected>Нейтральное</option>
                                <option value="happy">Радостное</option>
                            </select>
                        </div>
                        
                        <div class="button-group">
                            <button class="btn-get" onclick="testGet()">GET запрос</button>
                            <button class="btn-post" onclick="testPost()">POST запрос</button>
                            <button class="btn-path" onclick="testPath()">Path параметр</button>
                        </div>
                        
                        <div id="result" class="result"></div>
                        
                        <div class="api-info">
                            <h4> Заголовок запроса (опционально):</h4>
                            <input type="text" id="apiKey" placeholder="API ключ (например: demo_key)" style="margin-top: 5px;">
                            <p style="margin-top: 10px; color: #666; font-size: 12px;">
                                Для демо используйте любой ключ, начинающийся с "demo_"
                            </p>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2> Документация API</h2>
                        
                        <div class="endpoints-grid">
                            <div class="endpoint-card">
                                <span class="badge">GET</span>
                                <h4>/api/v1/</h4>
                                <p>Информация о доступных эндпоинтах</p>
                            </div>
                            
                            <div class="endpoint-card">
                                <span class="badge">GET</span>
                                <h4>/api/v1/health</h4>
                                <p>Проверка здоровья приложения</p>
                            </div>
                            
                            <div class="endpoint-card">
                                <span class="badge">GET</span>
                                <h4>/api/v1/greet?name=...</h4>
                                <p>Приветствие через GET с query параметрами</p>
                            </div>
                            
                            <div class="endpoint-card">
                                <span class="badge">POST</span>
                                <h4>/api/v1/greet</h4>
                                <p>Приветствие через POST с JSON телом</p>
                            </div>
                            
                            <div class="endpoint-card">
                                <span class="badge">GET</span>
                                <h4>/api/v1/greet/{name}</h4>
                                <p>Приветствие с именем в пути URL</p>
                            </div>
                            
                            <div class="endpoint-card">
                                <span class="badge">GET</span>
                                <h4>/api/v1/service/info</h4>
                                <p>Информация о сервисе приветствий</p>
                            </div>
                        </div>
                        
                        <div style="margin-top: 20px;">
                            <a href="/docs" target="_blank" style="display: inline-block; padding: 12px 24px; background: #4CAF50; color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
                                 Открыть Swagger документацию
                            </a>
                            <a href="/redoc" target="_blank" style="display: inline-block; padding: 12px 24px; background: #2196F3; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; margin-left: 10px;">
                                 Открыть ReDoc документацию
                            </a>
                        </div>
                    </div>
                </div>
                
                <footer>
                    <p>FastAPI Параметр Приложение | Модульная архитектура | Версия 1.0.0</p>
                    <p>Тестовое приложение с разделением логики по слоям</p>
                </footer>
            </div>
            
            <script>
                async function testGet() {
                    const name = document.getElementById('name').value || 'Гость';
                    const language = document.getElementById('language').value;
                    const mood = document.getElementById('mood').value;
                    const apiKey = document.getElementById('apiKey').value;
                    
                    const url = `/api/v1/greet?name=${encodeURIComponent(name)}&language=${language}&mood=${mood}`;
                    
                    const headers = {};
                    if (apiKey) {
                        headers['X-API-Key'] = apiKey;
                    }
                    
                    try {
                        const response = await fetch(url, { headers });
                        const data = await response.json();
                        showResult('GET', data, response);
                    } catch (error) {
                        showError(error);
                    }
                }
                
                async function testPost() {
                    const name = document.getElementById('name').value || 'Гость';
                    const language = document.getElementById('language').value;
                    const mood = document.getElementById('mood').value;
                    const apiKey = document.getElementById('apiKey').value;
                    
                    const url = '/api/v1/greet';
                    
                    const headers = {
                        'Content-Type': 'application/json'
                    };
                    if (apiKey) {
                        headers['X-API-Key'] = apiKey;
                    }
                    
                    try {
                        const response = await fetch(url, {
                            method: 'POST',
                            headers: headers,
                            body: JSON.stringify({
                                name: name,
                                language: language,
                                mood: mood
                            })
                        });
                        const data = await response.json();
                        showResult('POST', data, response);
                    } catch (error) {
                        showError(error);
                    }
                }
                
                async function testPath() {
                    const name = document.getElementById('name').value || 'Гость';
                    const language = document.getElementById('language').value;
                    const mood = document.getElementById('mood').value;
                    const apiKey = document.getElementById('apiKey').value;
                    
                    const url = `/api/v1/greet/${encodeURIComponent(name)}?language=${language}&mood=${mood}`;
                    
                    const headers = {};
                    if (apiKey) {
                        headers['X-API-Key'] = apiKey;
                    }
                    
                    try {
                        const response = await fetch(url, { headers });
                        const data = await response.json();
                        showResult('PATH', data, response);
                    } catch (error) {
                        showError(error);
                    }
                }
                
                function showResult(method, data, response) {
                    const resultDiv = document.getElementById('result');
                    const time = new Date(data.timestamp).toLocaleTimeString();
                    const processTime = response.headers.get('X-Process-Time');
                    
                    let languageNames = {
                        'ru': 'Русский',
                        'en': 'English',
                        'es': 'Español',
                        'fr': 'Français'
                    };
                    
                    let moodNames = {
                        'formal': 'Формальное',
                        'neutral': 'Нейтральное',
                        'happy': 'Радостное',
                        'morning': 'Утреннее',
                        'day': 'Дневное',
                        'evening': 'Вечернее',
                        'night': 'Ночное'
                    };
                    
                    resultDiv.innerHTML = `
                        <h3> ${method} запрос выполнен успешно!</h3>
                        <div class="message">${data.message}</div>
                        <div class="details">
                            <p><strong>Метод:</strong> ${method}</p>
                            <p><strong>Время:</strong> ${time}</p>
                            <p><strong>Время обработки:</strong> ${processTime ? parseFloat(processTime).toFixed(3) + 's' : 'N/A'}</p>
                            <p><strong>Статус:</strong> ${response.status} ${response.statusText}</p>
                            <p><strong>Язык:</strong> ${languageNames[data.request_data.language] || data.request_data.language}</p>
                            <p><strong>Настроение:</strong> ${moodNames[data.request_data.mood] || data.request_data.mood}</p>
                            <p><strong>Оригинальное имя:</strong> ${data.request_data.original_name}</p>
                            <p><strong>Обработанное имя:</strong> ${data.request_data.processed_name}</p>
                        </div>
                    `;
                    resultDiv.classList.add('show');
                }
                
                function showError(error) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = `
                        <h3 style="color: #ffcccc;"> Ошибка!</h3>
                        <div class="details">
                            <p><strong>Сообщение:</strong> ${error.message || error}</p>
                            <p>Проверьте введенные данные и попробуйте снова.</p>
                        </div>
                    `;
                    resultDiv.classList.add('show');
                }
                
                // Тест при загрузке
                window.onload = async function() {
                    try {
                        const response = await fetch('/api/v1/health');
                        const data = await response.json();
                        console.log('Приложение запущено:', data);
                    } catch (error) {
                        console.log('Приложение загружается...');
                    }
                };
            </script>
        </body>
        </html>
        """
    
    return application


# Создаем экземпляр приложения
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print(f" Запуск {settings.APP_NAME} v{settings.VERSION}")
    print("=" * 60)
    print(f" Документация: http://localhost:8000{settings.DOCS_URL}")
    print(f" Альтернативная документация: http://localhost:8000{settings.REDOC_URL}")
    print(f" Веб-интерфейс: http://localhost:8000")
    print(f" Режим отладки: {'ВКЛ' if settings.DEBUG else 'ВЫКЛ'}")
    print("=" * 60)
    
    # Запуск сервера
    uvicorn.run(
        "main:app",  # Импорт как строка для поддержки reload
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
