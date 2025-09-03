import requests
from core.utils.config import DEEPSEEK_API_KEY, API_URL, DEEPSEEK_MODEL
from core.utils.prompt import SYSTEM_PROMPT, OFF_TOPIC_RESPONSE, AUTO_RELEVANCE_SYSTEM_PROMPT

def is_off_topic(message: str) -> bool:
    """
    Определяет, является ли сообщение отвлеченной темой при помощи DeepSeek-классификации.
    Возвращает True, если сообщение НЕ относится к теме авто/регистрации обращения.
    """
    try:
        if not message or not message.strip():
            return False
        # Если API ключ не настроен, не блокируем пользователя
        if DEEPSEEK_API_KEY == "ваш_deepseek_api_key" or not DEEPSEEK_API_KEY:
            return False
        messages = [
            {"role": "system", "content": AUTO_RELEVANCE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Текст: {message}\nОтветь только YES или NO."}
        ]
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": DEEPSEEK_MODEL,
            "messages": messages
        }
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        if response.ok:
            raw = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            label = (raw or "").strip().upper()
            is_relevant = label.startswith("YES")
            return not is_relevant
        return False
    except Exception as e:
        print(f"Ошибка при классификации релевантности: {e}")
        return False

def ask_ai(user_message: str, history=None) -> str:
    if history is None:
        history = []
    
    # Проверяем, не является ли сообщение отвлеченной темой
    if is_off_topic(user_message):
        return OFF_TOPIC_RESPONSE
    
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

def fix_grammar(text: str) -> str:
    """
    Исправляет грамматику текста с помощью DeepSeek
    """
    # Проверяем, есть ли API ключ
    if DEEPSEEK_API_KEY == "ваш_deepseek_api_key" or not DEEPSEEK_API_KEY:
        print("⚠️ API ключ DeepSeek не настроен. Возвращаю исходный текст.")
        return text
    
    prompt = f"""
    Исправь грамматические ошибки в следующем тексте на русском языке.
    
    Правила исправления:
    - НЕ МЕНЯЙ смысл, содержание или структуру предложения
    - Исправляй ТОЛЬКО грамматические ошибки (падежи, спряжения, согласования)
    - Исправляй склонения существительных и прилагательных
    - Исправляй спряжения глаголов
    - Сохраняй разговорный стиль речи
    - НЕ добавляй лишние слова
    
    Текст: {text}
    
    Верни только исправленный текст без дополнительных комментариев.
    """
    
    try:
        messages = [
            {"role": "system", "content": "Ты помощник для исправления грамматических ошибок. Исправляй только грамматику, не меняя смысл."},
            {"role": "user", "content": prompt}
        ]
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": DEEPSEEK_MODEL,
            "messages": messages
        }
        print(f"🔧 Отправляю запрос к DeepSeek API...")
        print(f"🔧 URL: {API_URL}")
        print(f"🔧 Модель: {DEEPSEEK_MODEL}")
        response = requests.post(API_URL, json=data, headers=headers)
        print(f"🔧 Статус ответа: {response.status_code}")
        
        if response.ok:
            response_data = response.json()
            print(f"🔧 Ответ API: {response_data}")
            corrected_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", text)
            return corrected_text.strip()
        else:
            print(f"❌ Ошибка при исправлении грамматики: {response.status_code}")
            print(f"❌ Текст ошибки: {response.text}")
            return text
    except Exception as e:
        print(f"Ошибка при исправлении грамматики: {e}")
        return text 