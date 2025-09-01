from aiogram import Router, types
from aiogram.filters import Command

admin_router = Router(name="admin_router")

@admin_router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer("admin: заглушка") 