from core.handlers import core_message_router
from core.handlers.voice import router as voice_router
from core.handlers.callback.help import router as help_router
from menu.routers import menu_routers
from admin.routers import admin_routers

routers = [
    voice_router,  # Голосовые сообщения обрабатываем первыми
    core_message_router,
    help_router,
    *menu_routers,
    *admin_routers
] 