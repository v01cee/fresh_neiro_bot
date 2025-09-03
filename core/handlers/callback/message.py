import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.services.ai import ask_ai
from core.utils.ai import validate_phone, format_phone
from core.handlers.state.dialog import ClientDialog
from core.utils.messages import *
from core.utils.summary import create_problem_summary, update_problem_summary, create_solution_summary, update_solution_summary
from core.services.webhook import send_client_data_to_webhook, format_client_data_for_webhook

router = Router(name="core_message_router")

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start - сбрасывает диалог и приветствует пользователя
"""
    await state.clear()
    await message.answer(WELCOME_MESSAGE)
    await state.set_state(ClientDialog.waiting_for_name)

@router.message()
async def handle_message(message: types.Message, state: FSMContext):
    """
    Обработчик всех текстовых сообщений с пошаговым диалогом
    """
    # Проверяем, что это текстовое сообщение
    if not message.text:
        # Если это не текстовое сообщение (например, голосовое), игнорируем
        # Голосовые сообщения обрабатываются в voice.py
        return
    
    user_message = message.text.strip()
    
    # Получаем текущее состояние диалога
    current_state = await state.get_state()
    
    # Если это первое сообщение, начинаем диалог
    if not current_state:
        await cmd_start(message, state)
        return
    
    # Обработка в зависимости от текущего состояния
    if current_state == ClientDialog.waiting_for_name.state:
        await handle_name_step(message, state, user_message)
        
    elif current_state == ClientDialog.waiting_for_phone.state:
        await handle_phone_step(message, state, user_message)
        
    elif current_state == ClientDialog.waiting_for_details.state:
        await handle_details_step(message, state, user_message)
        
    elif current_state == ClientDialog.waiting_for_confirmation.state:
        await handle_confirmation_step(message, state, user_message)
        
    elif current_state == ClientDialog.waiting_for_solution.state:
        await handle_solution_step(message, state, user_message)
        
    elif current_state == ClientDialog.waiting_for_solution_confirmation.state:
        await handle_solution_confirmation_step(message, state, user_message)

async def handle_name_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага ввода имени"""
    # Проверяем, что введено имя (минимум 2 слова)
    name_parts = user_message.split()
    if len(name_parts) < 2:
        await message.answer(NAME_REQUEST)
        return
    
    # Сохраняем имя
    await state.update_data(client_name=user_message)
    
    # Переходим к следующему шагу
    await message.answer(PHONE_REQUEST_TEMPLATE)
    await state.set_state(ClientDialog.waiting_for_phone)

async def handle_phone_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага ввода телефона"""
    if validate_phone(user_message):
        formatted_phone = format_phone(user_message)
        await state.update_data(client_phone=formatted_phone)
        
        # Переходим к деталям проблемы (извинение + запрос деталей)
        await message.answer(TOPIC_REQUEST)
        await state.set_state(ClientDialog.waiting_for_details)
    else:
        await message.answer(PHONE_ERROR)



async def handle_details_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага ввода деталей обращения"""
    await state.update_data(client_details=user_message)
    
    # Получаем все собранные данные
    data = await state.get_data()
    
    # Создаем резюме проблемы (используем детали как тему и детали)
    summary = create_problem_summary("Проблема клиента", user_message)
    
    # Сохраняем резюме в состоянии
    await state.update_data(problem_summary=summary)
    
    # Формируем подтверждение с резюме
    confirmation_text = CONFIRMATION_TEMPLATE.format(summary=summary)
    await message.answer(confirmation_text)
    await state.set_state(ClientDialog.waiting_for_confirmation)

async def handle_confirmation_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага подтверждения"""
    user_response = user_message.lower().strip()
    
    if user_response in POSITIVE_ANSWERS:
        # Переходим к запросу решения
        await message.answer(SOLUTION_REQUEST)
        await state.set_state(ClientDialog.waiting_for_solution)
        
    elif user_response in NEGATIVE_ANSWERS:
        # Возвращаемся на предыдущий шаг - запрос деталей проблемы
        await message.answer("Хорошо, давайте исправим. " + TOPIC_REQUEST)
        await state.set_state(ClientDialog.waiting_for_details)
        
    else:
        # Обрабатываем как уточнение
        data = await state.get_data()
        original_summary = data.get('problem_summary', '')
        
        # Создаем новое резюме на основе уточнения
        new_summary = update_problem_summary(original_summary, user_message)
        
        # Сохраняем обновленное резюме
        await state.update_data(problem_summary=new_summary)
        
        # Отправляем обновленное подтверждение
        confirmation_text = CONFIRMATION_UPDATE_TEMPLATE.format(summary=new_summary)
        await message.answer(confirmation_text)

async def handle_solution_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага предложения решения"""
    # Сохраняем предложение решения
    await state.update_data(client_solution=user_message)
    
    # Создаем резюме предложения решения
    summary = create_solution_summary(user_message)
    
    # Сохраняем резюме в состоянии
    await state.update_data(solution_summary=summary)
    
    # Формируем подтверждение с резюме
    confirmation_text = SOLUTION_CONFIRMATION_TEMPLATE.format(summary=summary)
    await message.answer(confirmation_text)
    await state.set_state(ClientDialog.waiting_for_solution_confirmation)

async def handle_solution_confirmation_step(message: types.Message, state: FSMContext, user_message: str):
    """Обработка шага подтверждения предложения решения"""
    user_response = user_message.lower().strip()
    
    if user_response in POSITIVE_ANSWERS:
        # Получаем все данные клиента
        data = await state.get_data()
        print(f"📋 Данные клиента из состояния: {data}")
        
        # Форматируем данные для вебхука
        client_data = format_client_data_for_webhook(
            name=data.get('client_name', ''),
            phone=data.get('client_phone', ''),
            problem_description=data.get('client_details', ''),
            client_offer=data.get('client_solution', '')
        )
        
        # Отправляем данные на вебхук
        print("🚀 Отправляю данные на вебхук...")
        webhook_success = send_client_data_to_webhook(client_data)
        print(f"📊 Результат отправки: {'✅ Успешно' if webhook_success else '❌ Ошибка'}")
        
        # Всегда показываем успешное сообщение, независимо от результата вебхука
        await message.answer(SUCCESS_TEMPLATE)
        
        # Очищаем состояние
        await state.clear()
        
    elif user_response in NEGATIVE_ANSWERS:
        # Возвращаемся на предыдущий шаг - запрос предложения решения
        await message.answer("Хорошо, давайте исправим. " + SOLUTION_REQUEST)
        await state.set_state(ClientDialog.waiting_for_solution)
        
    else:
        # Обрабатываем как уточнение
        data = await state.get_data()
        original_summary = data.get('solution_summary', '')
        
        # Создаем новое резюме на основе уточнения
        new_summary = update_solution_summary(original_summary, user_message)
        
        # Сохраняем обновленное резюме
        await state.update_data(solution_summary=new_summary)
        
        # Отправляем обновленное подтверждение
        confirmation_text = SOLUTION_CONFIRMATION_UPDATE_TEMPLATE.format(summary=new_summary)
        await message.answer(confirmation_text) 