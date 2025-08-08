import functools
from aiogram.types import Message, CallbackQuery
from .exceptions import TokenNotFoundError


def require_auth(redirect_to_auth: bool = True):
    def decorator(handler):
        @functools.wraps(handler)
        async def wrapper(event, *args, **kwargs):    
            try:
                return await handler(event, *args, **kwargs)
            except TokenNotFoundError:
                if redirect_to_auth:
                    from handlers.common import show_auth_menu
                    await show_auth_menu(event, error_message="⚠️ Необходимо войти в систему")
                else:
                    await event.answer(
                        "❌ Вы не авторизованы. Войдите в систему для выполнения этого действия.",
                        show_alert=True
                    )
        return wrapper
    return decorator