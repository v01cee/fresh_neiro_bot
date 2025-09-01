from aiogram import Router, F
from aiogram.types import Message, Voice
from aiogram.fsm.context import FSMContext
from core.services.audio import audio_processor
from core.services.ai import fix_grammar
from core.handlers.state.dialog import ClientDialog
from core.handlers.callback.message import (
    handle_details_step, 
    handle_confirmation_step, 
    handle_solution_step, 
    handle_solution_confirmation_step
)

router = Router(name="voice_handler")

@router.message(F.voice)
async def handle_voice_message(message: Message, state: FSMContext):
    """Обработка голосовых сообщений"""
    
    print(f"🎤 Получено голосовое сообщение от пользователя {message.from_user.id}")
    
    # Проверяем готовность модели
    if not audio_processor.is_model_ready():
        print("❌ Модель Vosk не готова")
        await message.answer("🔄 Модель распознавания речи еще загружается. Попробуйте через несколько секунд.")
        return
    
    # Получаем текущее состояние диалога
    current_state = await state.get_state()
    print(f"📊 Текущее состояние диалога: {current_state}")
    
    # Обрабатываем голосовое сообщение с 3-го по 6-й шаг (после изменений в структуре диалога)
    allowed_states = [
        ClientDialog.waiting_for_details.state,
        ClientDialog.waiting_for_confirmation.state,
        ClientDialog.waiting_for_solution.state,
        ClientDialog.waiting_for_solution_confirmation.state
    ]
    
    print(f"✅ Разрешенные состояния: {allowed_states}")
    
    if current_state not in allowed_states:
        print(f"❌ Состояние {current_state} не разрешено для голосовых сообщений")
        await message.answer("🎤 Голосовые сообщения принимаются только с 3-го по 6-й шаг. Пожалуйста, используйте текстовое сообщение для продолжения диалога.")
        return
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer("🎤 Обрабатываю голосовое сообщение...")
    print("🎤 Начинаю обработку голосового сообщения...")
    
    try:
        # Распознаем речь
        print("🎤 Вызываю audio_processor.process_voice_message...")
        recognized_text = await audio_processor.process_voice_message(message.voice, message.bot)
        
        print(f"🎤 Результат распознавания: '{recognized_text}'")
        
        if not recognized_text:
            print("❌ Распознанный текст пустой")
            await processing_msg.edit_text("❌ Не удалось распознать речь. Попробуйте еще раз или отправьте текстовое сообщение.")
            return
        
        # Исправляем грамматику распознанного текста
        print("🔧 Исправляю грамматику...")
        corrected_text = fix_grammar(recognized_text)
        print(f"🔧 Исправленный текст: '{corrected_text}'")
        
        # Убираем сообщение о начале обработки
        print("✅ Удаляю сообщение о начале обработки")
        await processing_msg.delete()
        
        # Используем исправленный текст для дальнейшей обработки
        final_text = corrected_text
        
        # Обрабатываем как обычное текстовое сообщение в зависимости от текущего шага
        if current_state == ClientDialog.waiting_for_details.state:
            await handle_details_step(message, state, final_text)
        elif current_state == ClientDialog.waiting_for_confirmation.state:
            await handle_confirmation_step(message, state, final_text)
        elif current_state == ClientDialog.waiting_for_solution.state:
            await handle_solution_step(message, state, final_text)
        elif current_state == ClientDialog.waiting_for_solution_confirmation.state:
            await handle_solution_confirmation_step(message, state, final_text)
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ Произошла ошибка при обработке голосового сообщения: {str(e)}")
        print(f"Ошибка в обработке голосового сообщения: {e}")

@router.message(F.audio)
async def handle_audio_message(message: Message, state: FSMContext):
    """Обработка аудио файлов (только на шаге деталей)"""
    
    # Получаем текущее состояние диалога
    current_state = await state.get_state()
    
    # Обрабатываем аудио файлы с 3-го по 6-й шаг (после изменений в структуре диалога)
    allowed_states = [
        ClientDialog.waiting_for_details.state,
        ClientDialog.waiting_for_confirmation.state,
        ClientDialog.waiting_for_solution.state,
        ClientDialog.waiting_for_solution_confirmation.state
    ]
    
    if current_state not in allowed_states:
        await message.answer("🎵 Аудио файлы принимаются только с 3-го по 6-й шаг. Пожалуйста, используйте текстовое сообщение для продолжения диалога.")
        return
    
    # Проверяем готовность модели
    if not audio_processor.is_model_ready():
        await message.answer("🔄 Модель распознавания речи еще загружается. Попробуйте через несколько секунд.")
        return
    
    # Отправляем сообщение о начале обработки
    processing_msg = await message.answer("🎵 Обрабатываю аудио файл...")
    
    try:
        # Для аудио файлов используем тот же процессор
        # (можно расширить для поддержки других форматов)
        await processing_msg.edit_text("⚠️ Обработка аудио файлов пока не поддерживается. Отправьте голосовое сообщение.")
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ Произошла ошибка при обработке аудио файла: {str(e)}")
        print(f"Ошибка в обработке аудио файла: {e}") 