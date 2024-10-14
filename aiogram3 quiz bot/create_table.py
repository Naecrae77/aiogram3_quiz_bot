async def create_table():
    # Create a connection to the database (if it does not exist, it will be created)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Execute an SQL query to the database
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')       
        # Save changes
        await db.commit()
