let currentTasks = [];
let initialized = false;

async function loadTasks() {
    console.log('loadTasks вызвана');
    try {
        const response = await fetch('/api/tasks');
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        currentTasks = await response.json();
        console.log('Задачи загружены:', currentTasks);
        displayTasks(currentTasks);
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        document.getElementById('tasksList').innerHTML =
            `<p style="color: red; padding: 20px; text-align: center;">
                Ошибка загрузки задач: ${error.message}
            </p>`;
    }
}

function displayTasks(tasks) {
    console.log('displayTasks вызвана с:', tasks);
    const container = document.getElementById('tasksList');

    if (!container) {
        console.error('Элемент tasksList не найден!');
        return;
    }

    if (!tasks || tasks.length === 0) {
        container.innerHTML =
            `<p style="padding: 20px; color: #666; text-align: center;">
                Нет задач. Добавьте первую!
            </p>`;
        return;
    }

    let html = '';
    tasks.forEach(task => {
        console.log(`Обработка задачи ${task.id}:`, task);
        html += `
        <div class="task ${task.completed ? 'completed' : ''}" id="task-${task.id}">
            <div class="task-title">${task.title}</div>
            <div class="task-actions">
                <button class="complete-btn" onclick="toggleTask(${task.id})">
                    ${task.completed ? '❌ Отменить' : '✅ Выполнить'}
                </button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">🗑️ Удалить</button>
            </div>
        </div>`;
    });

    container.innerHTML = html;
    console.log('Задачи отображены');
}

async function addTask() {
    console.log('addTask вызвана');
    const input = document.getElementById('taskInput');

    if (!input) {
        console.error('Поле ввода не найдено!');
        alert('Ошибка: поле ввода не найдено');
        return;
    }

    const title = input.value.trim();
    console.log('Введенный текст:', title);

    if (!title) {
        alert('Пожалуйста, введите задачу!');
        input.focus();
        return;
    }

    try {
        console.log('Отправка запроса на создание задачи...');
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({title: title})
        });

        console.log('Ответ получен, статус:', response.status);
        const result = await response.json();
        console.log('Результат:', result);

        if (response.ok) {
            input.value = '';
            await loadTasks();
            alert('✅ Задача добавлена!');
        } else {
            alert('❌ Ошибка: ' + (result.error || 'Неизвестная ошибка'));
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('🚫 Ошибка сети: ' + error.message);
    }
}

async function toggleTask(taskId) {
    console.log('toggleTask вызвана для задачи:', taskId);

    try {
        const task = currentTasks.find(t => t.id === taskId);
        if (!task) {
            alert('Задача не найдена!');
            return;
        }

        console.log('Текущий статус:', task.completed);
        const newStatus = !task.completed;

        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({completed: newStatus})
        });

        console.log('Ответ сервера:', response.status);
        const result = await response.json();

        if (response.ok) {
            console.log('Задача обновлена:', result);
            await loadTasks();
            alert(`✅ Статус задачи "${task.title}" изменен!`);
        } else {
            alert('❌ Ошибка: ' + (result.error || 'Не удалось обновить задачу'));
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('🚫 Ошибка сети: ' + error.message);
    }
}

async function deleteTask(taskId) {
    console.log('deleteTask вызвана для задачи:', taskId);

    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
        console.log('Удаление отменено');
        return;
    }

    try {
        const task = currentTasks.find(t => t.id === taskId);
        const taskTitle = task ? task.title : 'задачу';

        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });

        console.log('Ответ сервера:', response.status);
        const result = await response.json();

        if (response.ok && result.success) {
            console.log('Задача удалена:', result);
            await loadTasks(); // Обновляем список
            alert(`🗑️ Задача "${taskTitle}" удалена!`);
        } else {
            alert('❌ Ошибка: ' + (result.error || 'Не удалось удалить задачу'));
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('🚫 Ошибка сети: ' + error.message);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOM ЗАГРУЖЕН ===');

    if (initialized) {
        console.log('Уже инициализировано, пропускаем');
        return;
    }

    initialized = true;

    const taskInput = document.getElementById('taskInput');
    if (taskInput) {
        taskInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                console.log('Нажата клавиша Enter');
                addTask();
            }
        });
        console.log('Обработчик Enter добавлен');
    }
    console.log('Запускаем loadTasks...');
    loadTasks();
});

async function testAPI() {
    console.log('=== ТЕСТИРОВАНИЕ API ===');
    try {
        const response = await fetch('/api/tasks');
        console.log('API тест - статус:', response.status);
        const data = await response.json();
        console.log('API тест - данные:', data);

        if (response.ok) {
            console.log('✅ API работает корректно');
        } else {
            console.error('❌ API вернул ошибку:', data);
        }
    } catch (error) {
        console.error('❌ Ошибка теста API:', error);
    }
}

testAPI();
