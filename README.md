# 📖 Diary - Веб-приложение для ведения дневника

#### Веб-приложение для создания и управления персональными записями дневника с системой тегов и аутентификацией.

## ✨ Возможности

- 🔐 **Аутентификация пользователей** (регистрация, вход, выход)
- 📝 **`CRUD` операции** с записями дневника
- 🏷️ **Система тегов** для организации записей
- 🎨 **Чистый UI** с `Bootstrap`
- 📱 **Адаптивный дизайн**
- 🐳 **`Docker`- контейнеризация**
- 🔄 **`CI/CD pipeline`** с `GitHub Actions`
- 🐘 **`PostgreSQL`** как основная БД

## 🛠️ Технологический стек

### Backend
- **`Python 3.12`**
- **`Django 4.2`** - основной веб-фреймворк
- **`Django REST Framework`** - для `API` (в будущем)
- **`Poetry`** - управление зависимостями
- **`Gunicorn`** - production WSGI сервер

### Frontend
- **`HTML5`** + **`Jinja2`** шаблоны
- **`Bootstrap 5`** - стилизация 
- **`JavaScript`** - интерактивность

### База данных
- **`PostgreSQL 15`** - основная production БД
- **`SQLite`** - для разработки

### Инфраструктура
- **`Docker`** - контейнеризация приложения
- **`Docker Compose`** - оркестрация контейнеров
- **`GitHub Actions`** - `CI/CD pipeline`
- **`Nginx`** - `reverse proxy` (в production)

## 🚀 Быстрый старт

### Предварительные требования
- `Python 3.12`
- `Poetry`
- `PostgreSQL` (для production)
- `Docker` (для деплоя)

### 1. Клонирование репозитория
```
git clone https://github.com/karim-mir/Diary.git
```

### 2. Установка зависимостей
```commandline
poetry install
```

### 3. Настройка окружения
Создайте файл `.env` в корневой директории:
```commandline
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=diary_db
DB_USER=diary_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Миграции базы данных
```commandline
poetry run python manage.py migrate
```

### 5. Запуск `development` сервера
```commandline
poetry run python manage.py runserver
```
Приложение будет доступно по адресу: http://localhost:8000

## 🐳 Запуск через `Docker`

### Сборка и запуск:
```commandline
docker build -t diary-app .
docker run -p 8000:8000 diary-app
```

### Или с Docker Compose:
```commandline
docker-compose up --build
```

## 🔧 Конфигурация

### Переменные окружения

```
Переменная	Описание	        По умолчанию
SECRET_KEY	Секретный ключ Django	Обязательно
DEBUG	        Режим отладки	        False
DB_NAME	        Имя базы данных	        diary_db
DB_USER	        Пользователь БД	        diary_user
DB_PASSWORD	Пароль БД	        Обязательно
DB_HOST	        Хост БД	                localhost
DB_PORT	        Порт БД	                5432
```

## 🧪 Тестирование

### Запуск тестов
```commandline
poetry run python manage.py test
```

### Запуск с coverage
```commandline
coverage run manage.py test
coverage report
```

## 🔄 CI/CD Pipeline

### Проект использует GitHub Actions для автоматизации:

- ✅ Автоматическое тестирование при `push/pull` request

- 🐳 Сборка `Docker` образа

- 🚀 Автоматический деплой на сервер

- 🌐 `API Endpoints`

```
Метод	Endpoint	        Описание
GET	/                       Главная страница
GET	/entries/	        Список всех записей
GET	/entries/create/        Создание новой записи
GET	/entries/<id>/	        Детали записи
GET	/entries/<id>/edit/	Редактирование записи
POST    /entries/<id>/delete/	Удаление записи
GET	/tags/	                Список тегов
GET	/register/	        Регистрация
GET	/login/	                Вход
GET	/logout/	        Выход
```

## 🤝 Разработка

### Установка для разработки

```commandline
git clone https://github.com/karim-mir/Diary.git
cd Diary
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Создание миграций
```commandline
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

### Создание суперпользователя
```commandline
poetry run python manage.py createsuperuser
```

## 📝 Лицензия

### Этот проект лицензирован под `MIT License` - смотрите файл `LICENSE` для деталей.

### 👥 Автор
`Jalil Karimov`

`GitHub: @karim-mir`

### 🙏 Благодарности
Команда `Django` за отличный фреймворк

Сообщество `Bootstrap` за UI компоненты

Сообщество `Docker` за инструменты контейнеризации
