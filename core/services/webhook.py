import requests
import json
from datetime import datetime
from typing import Dict, Any

from settings import WEBHOOK_URL, WEBHOOK_API_KEY

# Альтернативные URL для тестирования
ALTERNATIVE_URLS = [
    "https://webhooks.freshauto.ru/api/handle_reclamation",
    "https://webhooks.freshauto.ru/webhook/handle_reclamation", 
    "https://webhooks.freshauto.ru/reclamation",
    "https://webhooks.freshauto.ru/api/reclamation"
]

def send_client_data_to_webhook(client_data: Dict[str, Any]) -> bool:
    """
    Отправляет данные клиента на вебхук
    
    Args:
        client_data: Словарь с данными клиента
        
    Returns:
        bool: True если отправка успешна, False если ошибка
    """
    try:
        # Формируем данные в нужном формате
        payload = {
            "name": client_data.get("name", ""),
            "surname": client_data.get("surname", ""),
            "phone": client_data.get("phone", ""),
            "problem_description": client_data.get("problem_description", ""),
            "client_offer": client_data.get("client_offer", ""),
            "date": client_data.get("date", datetime.now().strftime("%d.%m.%Y %H:%M")),
            "executions.executor": "customer_service"  # Пробуем другое значение
        }
        
        print(f"📤 Отправляю данные на вебхук:")
        print(f"📋 JSON данные: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        print(f"🌐 URL: {WEBHOOK_URL}")
        
        # Сначала проверим доступность сервера
        print(f"🔍 Проверяю доступность сервера...")
        try:
            check_response = requests.get("https://webhooks.freshauto.ru/", timeout=5)
            print(f"🔍 Сервер доступен, статус: {check_response.status_code}")
        except Exception as e:
            print(f"🔍 Ошибка подключения к серверу: {e}")
        
        # Попробуем GET запрос на endpoint
        print(f"🔍 Проверяю GET запрос на endpoint...")
        try:
            get_response = requests.get(WEBHOOK_URL, timeout=5)
            print(f"🔍 GET статус: {get_response.status_code}")
            print(f"🔍 GET ответ: {get_response.text[:200]}...")
        except Exception as e:
            print(f"🔍 GET ошибка: {e}")
        
        # Отправляем POST запрос
        print(f"📡 Отправляю POST запрос...")
        
        # Попробуем JSON
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # Если 404, попробуем с авторизацией
        if response.status_code == 404:
            print(f"🔄 Попробуем с авторизацией...")
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {WEBHOOK_API_KEY}",
                    "X-API-Key": WEBHOOK_API_KEY
                },
                timeout=10
            )
        
        # Если 404, попробуем form-data
        if response.status_code == 404:
            print(f"🔄 Попробуем отправить как form-data...")
            response = requests.post(
                WEBHOOK_URL,
                data=payload,
                timeout=10
            )
        
        # Если все еще 404, попробуем с другими заголовками
        if response.status_code == 404:
            print(f"🔄 Попробуем с другими заголовками...")
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "FreshAuto-Bot/1.0"
                },
                timeout=10
            )
        
        # Если все еще 404, попробуем альтернативные URL
        if response.status_code == 404:
            print(f"🔄 Пробуем альтернативные URL...")
            for alt_url in ALTERNATIVE_URLS:
                print(f"🔄 Тестирую: {alt_url}")
                try:
                    alt_response = requests.post(
                        alt_url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=5
                    )
                    if alt_response.status_code != 404:
                        print(f"✅ Найден рабочий URL: {alt_url}")
                        response = alt_response
                        break
                    else:
                        print(f"❌ {alt_url} - 404")
                except Exception as e:
                    print(f"❌ {alt_url} - ошибка: {e}")
        
        # Если все еще 404, попробуем другие HTTP методы
        if response.status_code == 404:
            print(f"🔄 Пробуем другие HTTP методы...")
            
            # Пробуем PUT
            try:
                put_response = requests.put(
                    WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                if put_response.status_code != 404:
                    print(f"✅ PUT работает: {put_response.status_code}")
                    response = put_response
                else:
                    print(f"❌ PUT - 404")
            except Exception as e:
                print(f"❌ PUT ошибка: {e}")
            
            # Пробуем PATCH
            if response.status_code == 404:
                try:
                    patch_response = requests.patch(
                        WEBHOOK_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=5
                    )
                    if patch_response.status_code != 404:
                        print(f"✅ PATCH работает: {patch_response.status_code}")
                        response = patch_response
                    else:
                        print(f"❌ PATCH - 404")
                except Exception as e:
                    print(f"❌ PATCH ошибка: {e}")
        
        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📄 Заголовки ответа: {dict(response.headers)}")
        
        # Если все еще 404, попробуем как query параметры
        if response.status_code == 404:
            print(f"🔄 Последняя попытка - как query параметры...")
            try:
                query_response = requests.post(
                    WEBHOOK_URL,
                    params=payload,
                    timeout=5
                )
                if query_response.status_code != 404:
                    print(f"✅ Query параметры работают: {query_response.status_code}")
                    response = query_response
                else:
                    print(f"❌ Query параметры - 404")
            except Exception as e:
                print(f"❌ Query параметры ошибка: {e}")
        
        if response.status_code == 200:
            print(f"✅ Данные успешно отправлены на вебхук")
            try:
                response_json = response.json()
                print(f"📝 JSON ответ: {response_json}")
            except:
                print(f"📝 Текстовый ответ: {response.text}")
            return True
        else:
            print(f"❌ Ошибка отправки данных: {response.status_code}")
            try:
                error_json = response.json()
                print(f"❌ JSON ошибки: {error_json}")
            except:
                print(f"❌ Текст ошибки: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при отправке данных на вебхук: {e}")
        return False

def format_client_data_for_webhook(
    name: str,
    phone: str,
    problem_description: str,
    client_offer: str = ""
) -> Dict[str, Any]:
    """
    Форматирует данные клиента для отправки на вебхук
    
    Args:
        name: Имя и фамилия клиента
        phone: Телефон клиента
        problem_description: Описание проблемы
        client_offer: Предложение клиента (опционально)
        
    Returns:
        Dict[str, Any]: Отформатированные данные
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