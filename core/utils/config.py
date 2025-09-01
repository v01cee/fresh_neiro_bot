import os
from dotenv import load_dotenv
from settings import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL

# Для обратной совместимости
API_URL = DEEPSEEK_API_URL

# Загружаем переменные окружения из .env файла
load_dotenv()

# API ключ DeepSeek из settings.py
# DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL импортируются из settings.py 