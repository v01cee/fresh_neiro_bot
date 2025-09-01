from aiogram import Router, types
from aiogram.filters import Command

router = Router(name="menu_router")

@router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("menu: заглушка") 