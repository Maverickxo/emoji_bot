import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReactionTypeEmoji
from config import TOKEN
from save_message_dict import save_message_data, cleanup_old_messages, load_messages_data, tracked_reactions, \
    find_message_by_id
from user_rep import add_user_if_not_exists, increment_repa_for_user, decrement_repa_for_user
from get_rep import get_all_users_with_repa

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command("i_repa"))
async def command_start_handler(message: types.Message) -> None:
    await message.delete()
    all_users = await get_all_users_with_repa()
    user_info = "\n".join([f"[{user[1]}] Репутация: {user[2]}" for user in all_users])
    msg = await message.answer(user_info)
    await asyncio.sleep(20)
    await msg.delete()


@dp.message()
async def handle_message(msg: Message):
    save_message_data(msg)
    cleanup_old_messages()
    load_messages_data()
    user_full_name = msg.from_user.full_name
    user_id = msg.from_user.id
    await add_user_if_not_exists(user_id, user_full_name)


@dp.message_reaction()
async def get_reaction(react: ReactionTypeEmoji):
    try:
        new_reaction = str(react.new_reaction[-1]).split("emoji=")[1].replace("'", "")
        if new_reaction in tracked_reactions:
            print('репа +1')
            print(react.message_id)
            message, sender_id = find_message_by_id(str(react.message_id))
            if message:
                print(f"Сообщение найдено. Идентификатор отправителя: {sender_id}")
                await increment_repa_for_user(int(sender_id))
            else:
                print("Сообщение не найдено.")

    except:
        old_reacrion = str(react.old_reaction[-1]).split("emoji=")[1].replace("'", "")
        if old_reacrion in tracked_reactions:
            print('репа -1')
            message, sender_id = find_message_by_id(str(react.message_id))
            if message:
                print(f"Сообщение найдено. Идентификатор отправителя: {sender_id}")
                await decrement_repa_for_user(int(sender_id))
            else:
                print("Сообщение не найдено.")


async def main() -> None:
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
