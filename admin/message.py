from aiogram import types, Dispatcher

async def admin_command(message: types.Message):
    await message.answer("Админ-панель. Доступ разрешён.")

def register_admin_message_handler(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=["admin"]) 