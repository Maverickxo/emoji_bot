import aiosqlite


async def get_all_users_with_repa():
    async with aiosqlite.connect('repa.db') as db:
        async with db.execute('SELECT sender_id, user_full_name, repa FROM messages ORDER BY repa DESC') as cursor:
            users = await cursor.fetchall()
            return users

