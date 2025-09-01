import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# API ключ DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-coder")

# URL вебхука для рекламаций
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://webhooks.freshauto.ru/handle_reclamation")

# API ключ для вебхука (если нужен)
WEBHOOK_API_KEY = os.getenv("WEBHOOK_API_KEY", "your_webhook_api_key_here") 