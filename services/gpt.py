import asyncio
import openai
from aiogram import Bot
from config import settings


client = openai.AsyncClient(api_key=settings.openai_token)


class GPT:

    async def create_theread(self) -> str:
        thread = await client.beta.threads.create()
        return thread.id

    async def create_file(self, file_bytes) -> str:
        file = await client.files.create(file=file_bytes,
                                         purpose='assistants')
        return file.id

    async def ask(self, question: str,
                  bot: Bot, user: int, assistant_id: str,
                  thread_id: str, file_ids: list = []):
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question,
            file_ids=file_ids
        )
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        while run.status == "queued" or run.status == "in_progress":
            run = await client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run.status == "failed":
                await bot.send_message(
                    chat_id=user,
                    text="Случилась ошибка, повторите попытку")
                return
            await asyncio.sleep(3)

        messages = await client.beta.threads.messages.list(
            thread_id=thread_id
        )
        await bot.send_message(chat_id=user,
                               text=messages.data[0].content[0].text.value)
