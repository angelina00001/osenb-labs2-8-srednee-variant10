from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.routes import router
import uvicorn

APP_CONFIG = {
    "title": "FastAPI Hello App",
    "version": "1.0.0",
    "debug": True
}


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_CONFIG["title"],
        version=APP_CONFIG["version"],
        debug=APP_CONFIG["debug"],
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def serve_frontend():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>FastAPI Hello App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #333; }
                .form-group {
                    margin-bottom: 15px;
                }
                input, select, button {
                    padding: 10px;
                    margin: 5px 0;
                    width: 100%;
                    box-sizing: border-box;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover { background-color: #45a049; }
                .result {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #e8f5e9;
                    border-radius: 5px;
                }
                .error {
                    background-color: #ffebee;
                    color: #c62828;
                }
                .endpoints {
                    margin-top: 30px;
                    padding: 15px;
                    background-color: #e3f2fd;
                    border-radius: 5px;
                    font-size: 14px;
                }
                code {
                    background-color: #f1f1f1;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 FastAPI Hello App</h1>
                <p>Простое приложение с разделением слоев</p>
                
                <div class="form-group">
                    <label for="name">Имя:</label>
                    <input type="text" id="name" placeholder="Введите ваше имя" value="Иван">
                </div>
                
                <div class="form-group">
                    <label for="language">Язык:</label>
                    <select id="language">
                        <option value="ru">Русский</option>
                        <option value="en">English</option>
                    </select>
                </div>
                
                <button onclick="getGreeting()">Получить приветствие (GET)</button>
                <button onclick="postGreeting()">Получить приветствие (POST)</button>
                
                <div id="result" class="result" style="display:none;"></div>
                
                <div class="endpoints">
                    <h4>Доступные эндпоинты:</h4>
                    <ul>
                        <li><a href="/docs" target="_blank">📚 Swagger документация</a></li>
                        <li><a href="/redoc" target="_blank">📖 ReDoc документация</a></li>
                        <li><code>GET /api/v1/health</code> - Проверка здоровья</li>
                        <li><code>GET /api/v1/greet?name=Иван</code> - Приветствие (GET)</li>
                        <li><code>POST /api/v1/greet</code> - Приветствие (POST)</li>
                        <li><code>GET /api/v1/languages</code> - Доступные языки</li>
                    </ul>
                </div>
            </div>
            
            <script>
                async function getGreeting() {
                    const name = document.getElementById('name').value || 'Гость';
                    const language = document.getElementById('language').value;
                    const url = `/api/v1/greet?name=${encodeURIComponent(name)}&language=${language}`;
                    
                    try {
                        const response = await fetch(url);
                        const data = await response.json();
                        showResult(data);
                    } catch (error) {
                        showError(error);
                    }
                }
                
                async function postGreeting() {
                    const name = document.getElementById('name').value || 'Гость';
                    const language = document.getElementById('language').value;
                    const url = '/api/v1/greet';
                    
                    try {
                        const response = await fetch(url, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({name: name, language: language})
                        });
                        const data = await response.json();
                        showResult(data);
                    } catch (error) {
                        showError(error);
                    }
                }
                
                function showResult(data) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = `
                        <h4>✅ Успешно!</h4>
                        <p><strong>${data.message}</strong></p>
                        <p><small>Время: ${new Date(data.timestamp).toLocaleString()}</small></p>
                        <p><small>Язык: ${data.data.language}</small></p>
                    `;
                    resultDiv.className = 'result';
                    resultDiv.style.display = 'block';
                }
                
                function showError(error) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = `<strong>❌ Ошибка:</strong> ${error.message || error}`;
                    resultDiv.className = 'result error';
                    resultDiv.style.display = 'block';
                }
            </script>
        </body>
        </html>
        """
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )
