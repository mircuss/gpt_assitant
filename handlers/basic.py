from aiogram import Router, F
from aiogram.types import Message

from services.gpt import GPT
from sql.repo import UserRepo

basic_router = Router()

async def new_chat(user_id: int, repo: UserRepo):
    gpt = GPT()
    thread_id = await gpt.create_theread()
    await repo.update(user_id=user_id,
                      chat_id=thread_id)


@basic_router.message(F.text == "/start")
async def start(message: Message, user: UserRepo) -> None:
    user_obj = await user.create(user_id=message.from_user.id,
                      fullname=message.from_user.full_name)
    if not user_obj.chat_id:
        await new_chat(user_id=message.from_user.id,
                    repo=user)
    await message.answer(text=("Вас приветствует ваш личный помощьник.\n"
                               "Напишите мне вопрос.\n"
                               "Для создания нового чата напишите /restart"))


@basic_router.message(F.text == "/restart")
async def restart(message: Message, user: UserRepo) -> None:
    await new_chat(user_id=message.from_user.id,
                   repo=user)
    await message.answer(text="Новый чат успешно создан.")
