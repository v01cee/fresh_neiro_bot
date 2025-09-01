"""
Утилиты для создания резюме проблемы с помощью AI
"""

from core.services.ai import ask_ai

def create_problem_summary(topic: str, details: str) -> str:
    """
    Создает резюме проблемы на основе темы и деталей
    """
    prompt = f"""
    Создай краткое резюме проблемы клиента на основе следующей информации:
    
    Тема: {topic}
    Детали: {details}
    
    Резюме должно быть:
    - Кратким (1-2 предложения)
    - Использовать ключевые слова клиента
    - Быть понятным и четким
    - Не добавлять лишней информации
    - Сохранять грамматическую правильность
    - Использовать правильные падежи и склонения
    
    Верни только резюме без дополнительных комментариев.
    """
    
    try:
        summary = ask_ai(prompt, [])
        return summary.strip()
    except Exception as e:
        # Fallback - простое резюме
        return f"{topic}: {details[:100]}{'...' if len(details) > 100 else ''}"

def update_problem_summary(original_summary: str, correction: str) -> str:
    """
    Обновляет резюме проблемы на основе уточнения клиента
    """
    prompt = f"""
    Обнови резюме проблемы на основе уточнения клиента:
    
    Текущее резюме: {original_summary}
    Уточнение клиента: {correction}
    
    Создай новое резюме, которое:
    - Учитывает уточнение клиента
    - Сохраняет ключевые моменты
    - Краткое и понятное
    - Использует слова клиента
    
    Верни только обновленное резюме без дополнительных комментариев.
    """
    
    try:
        summary = ask_ai(prompt, [])
        return summary.strip()
    except Exception as e:
        # Fallback - простое обновление
        return f"{original_summary} (уточнение: {correction[:50]})"

def create_solution_summary(solution: str) -> str:
    """
    Создает резюме предложения решения
    """
    prompt = f"""
    Создай краткое резюме предложения решения клиента:
    
    Предложение: {solution}
    
    Резюме должно быть:
    - Кратким (1-2 предложения)
    - Использовать ключевые слова клиента
    - Быть понятным и четким
    - Не добавлять лишней информации
    
    Верни только резюме без дополнительных комментариев.
    """
    
    try:
        summary = ask_ai(prompt, [])
        return summary.strip()
    except Exception as e:
        # Fallback - простое резюме
        return f"{solution[:100]}{'...' if len(solution) > 100 else ''}"

def update_solution_summary(original_summary: str, correction: str) -> str:
    """
    Обновляет резюме предложения решения на основе уточнения клиента
    """
    prompt = f"""
    Обнови резюме предложения решения на основе уточнения клиента:
    
    Текущее резюме: {original_summary}
    Уточнение клиента: {correction}
    
    Создай новое резюме, которое:
    - Учитывает уточнение клиента
    - Сохраняет ключевые моменты
    - Краткое и понятное
    - Использует слова клиента
    
    Верни только обновленное резюме без дополнительных комментариев.
    """
    
    try:
        summary = ask_ai(prompt, [])
        return summary.strip()
    except Exception as e:
        # Fallback - простое обновление
        return f"{original_summary} (уточнение: {correction[:50]})" 