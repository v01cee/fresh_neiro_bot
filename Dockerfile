FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libasound2-dev \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Создаем папку для логов
RUN mkdir -p /app/logs

# Устанавливаем права на выполнение
RUN chmod +x botmain.py

# Открываем порт (если понадобится)
EXPOSE 8000

# Команда запуска
CMD ["python", "botmain.py"] 