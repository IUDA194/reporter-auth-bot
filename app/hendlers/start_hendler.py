from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.base import StorageKey

from app.keyboards.inline.connect_keyboard import connect_keyboard

from app.backend.api_requests import send_signed_request

start_router = Router()

user_data = {}
user_ref = {}

@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    args = message.text.split(" ")
    payload = args[1] if len(args) > 1 else None

    try:
        uuid = None
        ref = None

        if payload and payload.startswith("uuid_"):
            parts = payload.split("_", 2)
            uuid = parts[1] if len(parts) >= 2 else None
            if len(parts) == 3 and parts[2].startswith("ref_"):
                ref = parts[2][4:]

        if uuid:
            user_data[message.from_user.id] = uuid
            user_ref[message.from_user.id] = ref
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [ InlineKeyboardButton(text="Подтвердить вход!", callback_data="join") ]
                ]
            )
            first_name = message.from_user.first_name or "Пользователь"
            await message.answer(f"Привет, {first_name}!", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        try:
            await message.delete()
        except:
            pass



@start_router.callback_query(lambda c: c.data == "join")
async def join_handler(callback_query: CallbackQuery):
    """Обрабатывает нажатие кнопки 'Присоединиться'"""
    user = callback_query.from_user
    if not user:
        await callback_query.answer("Ошибка: не удалось получить информацию о пользователе.", show_alert=True)
        return

    uuid = user_data.get(user.id, "Не найден")
    ref = user_ref.get(user.id, None)

    response = send_signed_request(user=user, uuid=uuid, referred_by=ref)

    try:
        if response == 200:
            await callback_query.answer('Вход успешно подтверждён!')
            await callback_query.message.delete()
        else:
            raise ValueError('Something wrong!')
    except Exception:
        await callback_query.answer("Произошла ошибка при отправке данных.", show_alert=True)

    await callback_query.answer()
