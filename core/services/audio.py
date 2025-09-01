import os
import json
import wave
import tempfile
from typing import Optional, Tuple
import vosk
import soundfile as sf
from aiogram.types import Voice, Audio

class AudioProcessor:
    def __init__(self):
        """Инициализация процессора аудио с Vosk моделью"""
        self.model_path = "vosk-model-small-ru"
        self.model = None
        self.initialize_model()
    
    def initialize_model(self):
        """Инициализация модели Vosk"""
        try:
            # Проверяем, есть ли уже скачанная модель
            if os.path.exists(self.model_path):
                self.model = vosk.Model(self.model_path)
                print(f"Модель Vosk загружена из {self.model_path}")
            else:
                print("Модель Vosk не найдена. Скачиваем...")
                self.download_model()
        except Exception as e:
            print(f"Ошибка при инициализации модели Vosk: {e}")
    
    def download_model(self):
        """Скачивание модели Vosk для русского языка"""
        import urllib.request
        import zipfile
        
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
        zip_path = "vosk-model-small-ru.zip"
        
        try:
            print("Скачивание модели Vosk...")
            urllib.request.urlretrieve(model_url, zip_path)
            
            print("Распаковка модели...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Переименовываем папку
            if os.path.exists("vosk-model-small-ru-0.22"):
                os.rename("vosk-model-small-ru-0.22", self.model_path)
            
            # Удаляем zip файл
            os.remove(zip_path)
            
            self.model = vosk.Model(self.model_path)
            print("Модель Vosk успешно загружена!")
            
        except Exception as e:
            print(f"Ошибка при скачивании модели: {e}")
    
    async def process_voice_message(self, voice: Voice, bot) -> Optional[str]:
        """Обработка голосового сообщения и извлечение текста"""
        try:
            print("🎤 Начинаю обработку голосового сообщения в AudioProcessor")
            print(f"🎤 Модель Vosk готова: {self.model is not None}")
            if self.model:
                print(f"🎤 Путь к модели: {self.model_path}")
            # Скачиваем голосовое сообщение
            print("🎤 Скачиваю голосовое сообщение...")
            voice_file = await bot.get_file(voice.file_id)
            voice_bytes = await bot.download_file(voice_file.file_path)
            voice_bytes = voice_bytes.read()
            print(f"🎤 Скачано {len(voice_bytes)} байт")
            
            # Сохраняем во временный файл
            print("🎤 Сохраняю во временный файл...")
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
                temp_file.write(voice_bytes)
                temp_path = temp_file.name
            print(f"🎤 Временный файл: {temp_path}")
            
            # Конвертируем в WAV и распознаем
            print("🎤 Конвертирую и распознаю...")
            text = self.convert_and_recognize(temp_path)
            
            # Удаляем временный файл
            print("🎤 Удаляю временный файл...")
            os.unlink(temp_path)
            
            return text
            
        except Exception as e:
            print(f"❌ Ошибка при обработке голосового сообщения: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def convert_and_recognize(self, audio_path: str) -> Optional[str]:
        """Конвертация аудио в WAV и распознавание речи"""
        try:
            print("🎤 Начинаю конвертацию и распознавание...")
            # Конвертируем OGG в WAV
            wav_path = self.convert_to_wav(audio_path)
            
            if not wav_path:
                print("❌ Не удалось конвертировать в WAV")
                return None
            
            print(f"✅ WAV файл создан: {wav_path}")
            
            # Распознаем речь
            print("🎤 Начинаю распознавание речи...")
            text = self.recognize_speech(wav_path)
            print(f"🎤 Результат распознавания: '{text}'")
            
            # Удаляем временный WAV файл
            os.unlink(wav_path)
            print("✅ Временный WAV файл удален")
            
            return text
            
        except Exception as e:
            print(f"❌ Ошибка при конвертации и распознавании: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def convert_to_wav(self, audio_path: str) -> Optional[str]:
        """Конвертация аудио файла в WAV формат"""
        try:
            print(f"🎤 Конвертирую файл: {audio_path}")
            # Читаем аудио файл
            data, samplerate = sf.read(audio_path)
            print(f"🎤 Аудио данные: {len(data)} сэмплов, частота: {samplerate} Hz")
            
            # Создаем временный WAV файл
            wav_path = audio_path.replace('.ogg', '.wav')
            print(f"🎤 WAV путь: {wav_path}")
            
            # Конвертируем в 16kHz для Vosk
            if samplerate != 16000:
                print(f"🎤 Конвертирую частоту с {samplerate} Hz в 16000 Hz")
                import librosa
                data = librosa.resample(data, orig_sr=samplerate, target_sr=16000)
                samplerate = 16000
            
            # Сохраняем как WAV
            sf.write(wav_path, data, samplerate, subtype='PCM_16')
            print("✅ WAV файл сохранен с частотой 16kHz")
            
            return wav_path
            
        except Exception as e:
            print(f"❌ Ошибка при конвертации в WAV: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def recognize_speech(self, wav_path: str) -> Optional[str]:
        """Распознавание речи из WAV файла"""
        try:
            if not self.model:
                print("❌ Модель Vosk не инициализирована")
                return None
            
            print("✅ Модель Vosk готова")
            
            # Создаем распознаватель
            rec = vosk.KaldiRecognizer(self.model, 16000)
            print("✅ Распознаватель создан")
            
            # Читаем WAV файл
            print("🎤 Читаю WAV файл...")
            with wave.open(wav_path, 'rb') as wf:
                frames_count = 0
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    rec.AcceptWaveform(data)
                    frames_count += 1
                print(f"🎤 Обработано {frames_count} фреймов")
            
            # Получаем результат
            print("🎤 Получаю результат распознавания...")
            result = json.loads(rec.FinalResult())
            print(f"🎤 Сырой результат: {result}")
            text = result.get('text', '').strip()
            print(f"🎤 Извлеченный текст: '{text}'")
            
            return text if text else None
            
        except Exception as e:
            print(f"❌ Ошибка при распознавании речи: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def is_model_ready(self) -> bool:
        """Проверка готовности модели"""
        return self.model is not None

# Создаем глобальный экземпляр процессора
audio_processor = AudioProcessor() 