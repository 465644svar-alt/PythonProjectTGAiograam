import sqlite3

conn = sqlite3.connect('bot.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLA IF NOT EXIST users (
id INTEGER PRIMARY KEY,
username TEXT,
chat_id INTEGER)''')

conn.commit()
conn.close()
