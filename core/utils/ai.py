import requests
from core.utils.prompt import SYSTEM_PROMPT
from core.utils.config import DEEPSEEK_API_KEY, API_URL, DEEPSEEK_MODEL
import re

def ask_ai(user_message: str, history=None) -> str:
    if history is None:
        history = []
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message}
    ]
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": messages
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.ok:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа от нейросети.")
    return "Ошибка при обращении к ИИ-сервису."

def validate_phone(phone: str) -> bool:
    """
    Валидирует формат телефона: +7 XXX XXX XX XX или 8 XXX XXX XX XX
    """
    # Убираем все пробелы, дефисы, скобки
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Проверяем форматы: +7XXXXXXXXX или 8XXXXXXXXX (10 цифр после кода)
    if re.match(r'^\+7\d{10}$', phone_clean):
        return True
    elif re.match(r'^8\d{10}$', phone_clean):
        return True
    
    return False

def format_phone(phone: str) -> str:
    """
    Форматирует телефон в читаемый вид
    """
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    if phone_clean.startswith('+7'):
        return f"+7 {phone_clean[2:5]} {phone_clean[5:8]} {phone_clean[8:10]} {phone_clean[10:12]}"
    elif phone_clean.startswith('8'):
        return f"8 {phone_clean[1:4]} {phone_clean[4:7]} {phone_clean[7:9]} {phone_clean[9:11]}"
    
    return phone 