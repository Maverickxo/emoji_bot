import aiosqlite
import asyncio


async def add_user_if_not_exists(user_id, user_full_name):
    async with aiosqlite.connect('repa.db') as db:
        async with db.execute('SELECT 1 FROM messages WHERE sender_id = ?', (user_id,)) as cursor:
            user_exists = await cursor.fetchone()

        if not user_exists:
            user_full_name_str = str(user_full_name)
            await db.execute('INSERT INTO messages (sender_id, user_full_name) VALUES (?, ?)',
                             (user_id, user_full_name_str))
            await db.commit()
            print(f"Пользователь {user_full_name_str} (ID: {user_id}) добавлен в базу данных.")


async def increment_repa_for_user(sender_id):
    async with aiosqlite.connect('repa.db') as db:
        async with db.execute('SELECT repa FROM messages WHERE sender_id = ?', (sender_id,)) as cursor:
            user_data = await cursor.fetchone()
        if user_data:
            current_repa = user_data[0]
            new_repa = current_repa + 1
            await db.execute('UPDATE messages SET repa = ? WHERE sender_id = ?', (new_repa, sender_id))
            await db.commit()
            print(f"Значение repa для пользователя с ID {sender_id} увеличено до {new_repa}.")
        else:
            print(f"Пользователь с ID {sender_id} не найден в базе данных.")


async def decrement_repa_for_user(sender_id):
    async with aiosqlite.connect('repa.db') as db:
        async with db.execute('SELECT repa FROM messages WHERE sender_id = ?', (sender_id,)) as cursor:
            user_data = await cursor.fetchone()

        if user_data:
            current_repa = user_data[0]
            new_repa = current_repa - 1
            await db.execute('UPDATE messages SET repa = ? WHERE sender_id = ?', (new_repa, sender_id))
            await db.commit()
            print(f"Значение repa для пользователя с ID {sender_id} уменьшено до {new_repa}.")
        else:
            print(f"Пользователь с ID {sender_id} не найден в базе данных.")

# async def main():
#     async with aiosqlite.connect('repa.db') as db:
#         await db.execute('''
#             CREATE TABLE IF NOT EXISTS messages (
#                 id INTEGER PRIMARY KEY,
#                 user_full_name  TEXT,
#                 sender_id INTEGER,
#                 repa INTEGER DEFAULT 0
#             )
#         ''')
#         await db.commit()
#
#
# asyncio.run(main())
