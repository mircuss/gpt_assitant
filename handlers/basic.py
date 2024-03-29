from aiogram import Router, F
from aiogram.types import Message

from services.gpt import GPT
from sql.repo import UserRepo

basic_router = Router()


@basic_router.message(F.text == "/start")
async def start(message: Message, user: UserRepo) -> None:
    await user.create(user_id=message.from_user.id,
                      fullname=message.from_user.full_name)
    await message.answer(text=("Вас приветствует ваш личный помощьник.\n"
                               "Напишите мне вопрос.\n"
                               "Для создания нового чата напишите /restart"))


@basic_router.message(F.text == "/restart")
async def restart(message: Message, user: UserRepo) -> None:
    gpt = GPT()
    thread_id = await gpt.create_theread()
    await user.update(user_id=message.from_user.id,
                      chat_id=thread_id)
    await message.answer(text="Новый чат успешно создан.")
