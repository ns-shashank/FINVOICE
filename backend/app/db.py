import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("finvoice.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    amount REAL,
                    date TEXT)''')
    conn.commit()
    conn.close()

def add_expense(category, amount):
    conn = sqlite3.connect("finvoice.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
              (category, amount, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect("finvoice.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    data = c.fetchall()
    conn.close()
    return [{"id": x[0], "category": x[1], "amount": x[2], "date": x[3]} for x in data]
