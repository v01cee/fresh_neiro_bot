from aiogram.fsm.state import StatesGroup, State

class ClientDialog(StatesGroup):
    waiting_for_name = State()  # Шаг 1: Запрос Имени и Фамилии
    waiting_for_phone = State()  # Шаг 2: Запрос мобильного телефона
    waiting_for_details = State()  # Шаг 3: Детали обращения (извинение + запрос)
    waiting_for_confirmation = State()  # Шаг 4: Подтверждение
    waiting_for_solution = State()  # Шаг 5: Предложение решения
    waiting_for_solution_confirmation = State()  # Шаг 6: Подтверждение предложения 