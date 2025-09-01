#!/usr/bin/env python3
"""
Скрипт для инициализации модели Vosk
Запускается при первом запуске бота для скачивания модели распознавания речи
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def download_vosk_model():
    """Скачивание модели Vosk для русского языка"""
    model_path = "vosk-model-small-ru"
    
    # Проверяем, есть ли уже модель
    if os.path.exists(model_path):
        print(f"✅ Модель Vosk уже найдена в {model_path}")
        return True
    
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
    zip_path = "vosk-model-small-ru.zip"
    
    try:
        print("📥 Скачивание модели Vosk для русского языка...")
        print(f"URL: {model_url}")
        print("Это может занять несколько минут...")
        
        # Скачиваем файл
        urllib.request.urlretrieve(model_url, zip_path)
        
        print("📦 Распаковка модели...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Переименовываем папку
        if os.path.exists("vosk-model-small-ru-0.22"):
            os.rename("vosk-model-small-ru-0.22", model_path)
        
        # Удаляем zip файл
        os.remove(zip_path)
        
        print(f"✅ Модель Vosk успешно скачана и установлена в {model_path}")
        print("Теперь можно запускать бота!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при скачивании модели: {e}")
        return False

def check_dependencies():
    """Проверка необходимых зависимостей"""
    try:
        import vosk
        import soundfile
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости: {e}")
        print("Установите зависимости командой: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("🎤 Инициализация Vosk для распознавания речи")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Скачиваем модель
    if download_vosk_model():
        print("\n🎉 Инициализация завершена успешно!")
        print("Теперь можно запускать бота с поддержкой голосовых сообщений.")
    else:
        print("\n💥 Инициализация не удалась.")
        sys.exit(1) 