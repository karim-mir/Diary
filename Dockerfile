FROM python:3.12-slim

WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую папку
COPY . .

# Открываем порт для доступа к приложению
EXPOSE 8000

# Команда для запуска Django сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
