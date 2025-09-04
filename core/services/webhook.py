import requests
import json
from datetime import datetime
from typing import Dict, Any

from settings import WEBHOOK_URL, WEBHOOK_API_KEY


def send_client_data_to_webhook(client_data: Dict[str, Any]) -> bool:
    """
    Отправляет данные клиента на вебхук (только POST JSON на WEBHOOK_URL).
    """
    try:
        # Формируем данные в нужном формате
        payload = {
            "name": client_data.get("name", ""),
            "surname": client_data.get("surname", ""),
            "phone": client_data.get("phone", ""),
            "problem_description": client_data.get("problem_description", ""),
            "client_offer": client_data.get("client_offer", ""),
            "date": client_data.get("date", datetime.now().strftime("%d.%m.%Y %H:%M"))
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "FreshAuto-Bot/1.0"
        }
        # Добавляем ключ, если задан
        if WEBHOOK_API_KEY and WEBHOOK_API_KEY != "your_webhook_api_key_here":
            headers["Authorization"] = f"Bearer {WEBHOOK_API_KEY}"
            headers["X-API-Key"] = WEBHOOK_API_KEY

        print("📤 Отправляю данные на вебхук (POST JSON)...")
        print(f"🌐 URL: {WEBHOOK_URL}")
        print(f"📋 JSON данные: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        print(f"📊 Статус ответа: {response.status_code}")
        try:
            print(f"📝 Ответ: {response.json()}")
        except Exception:
            print(f"📝 Ответ (текст): {response.text}")

        if response.status_code in (200, 201, 202):
            print("✅ Данные успешно отправлены на вебхук")
            return True

        print("❌ Ошибка отправки данных на вебхук")
        return False

    except Exception as e:
        print(f"❌ Исключение при отправке данных на вебхук: {e}")
        return False


def format_client_data_for_webhook(
    name: str,
    phone: str,
    problem_description: str,
    client_offer: str = ""
) -> Dict[str, Any]:
    """
    Форматирует данные клиента для отправки на вебхук
    """
    # Разделяем имя и фамилию
    name_parts = name.strip().split()
    first_name = name_parts[0] if name_parts else ""
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    return {
        "name": first_name,
        "surname": last_name,
        "phone": phone,
        "problem_description": problem_description,
        "client_offer": client_offer,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    } 