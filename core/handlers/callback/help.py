from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.services.ai import ask_ai, is_off_topic
from core.handlers.state.dialog import ClientDialog
from core.utils.messages import *

router = Router(name="help_router")

@router.message(Command("help"))
async def cmd_help(message: types.Message, state: FSMContext):
    """Обработчик команды /help"""
    await message.answer(HELP_MESSAGE)

@router.message(F.text.lower().contains("помощь"))
@router.message(F.text.lower().contains("что делать"))
@router.message(F.text.lower().contains("как пользоваться"))
async def handle_help_request(message: types.Message, state: FSMContext):
    """Обработка запросов о помощи"""
    current_state = await state.get_state()
    
    if not current_state:
        await cmd_help(message, state)
        return
    
    # Определяем, на каком шаге находится пользователь
    step_info = {
        ClientDialog.waiting_for_name.state: "name",
        ClientDialog.waiting_for_phone.state: "phone",
        ClientDialog.waiting_for_topic.state: "topic",
        ClientDialog.waiting_for_details.state: "details",
        ClientDialog.waiting_for_confirmation.state: "confirmation",
        ClientDialog.waiting_for_solution.state: "solution",
        ClientDialog.waiting_for_solution_confirmation.state: "solution_confirmation"
    }
    
    current_step_key = step_info.get(current_state, "unknown")
    help_text = STEP_HELP_MESSAGES.get(current_step_key, "Неизвестный шаг")
    
    await message.answer(help_text)

@router.message(F.text.lower().contains("отмена"))
@router.message(F.text.lower().contains("отменить"))
@router.message(F.text.lower().contains("начать заново"))
async def handle_cancel_request(message: types.Message, state: FSMContext):
    """Обработка запросов на отмену/перезапуск"""
    await state.clear()
    await message.answer(CANCEL_MESSAGE) 