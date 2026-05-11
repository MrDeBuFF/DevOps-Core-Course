# Используем конкретную версию Python (slim — меньше размер, чем full)
FROM python:3.13-slim

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем curl
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Создаём non-root пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Рабочая директория
WORKDIR /app

# Копируем ТОЛЬКО зависимости сначала (важно для layer caching)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .

# Меняем владельца файлов
RUN chown -R appuser:appuser /app

# Переключаемся на non-root пользователя
USER appuser

# Документируем порт
EXPOSE 6000

# Команда запуска
CMD ["python", "app.py"]
