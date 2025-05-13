from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def connect_keyboard(client_id: str, ticket_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="Подключиться",
                                callback_data=f"connect_{client_id}_{ticket_id}")
    )

    return builder.as_markup()