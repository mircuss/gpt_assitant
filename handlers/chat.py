from aiogram import Router, F, Bot
from aiogram.types import Message

from sql.repo import UserRepo
from services.gpt import GPT

chat_router = Router()


@chat_router.message(F.text)
async def text(message: Message, user: UserRepo, bot: Bot) -> None:
    gpt = GPT()
    user_obj = await user.get(user_id=message.from_user.id)
    await gpt.ask(question=message.text,
                  bot=bot,
                  user=user_obj.id,
                  assistant_id="asst_1E7Zta6nw8EeM3VTiIieIfTR",
                  thread_id=user_obj.chat_id,
                  file_ids=[])
