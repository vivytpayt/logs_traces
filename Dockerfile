# Используем Python 3.11 slim
FROM python:3.11-slim

# Устанавливаем зависимости для сборки и работы
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения для uvicorn
ENV PYTHONUNBUFFERED=1

# По умолчанию запускаем gateway (можно переопределить командой в docker-compose)
#CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]