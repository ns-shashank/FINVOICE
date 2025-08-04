import speech_recognition as sr
import re
from datetime import datetime
import sqlite3

DB_PATH = "finvoice/finvoice.db"

def save_to_db(category, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                      (category TEXT, amount REAL, date TEXT)''')
    cursor.execute("INSERT INTO expenses VALUES (?, ?, ?)", (category, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def extract_expense(text):
    text = text.lower()

    # Extract amount
    amount_match = re.search(r'(\d+(\.\d+)?)', text)
    amount = float(amount_match.group()) if amount_match else 0.0

    # Clean up category
    # Remove known keywords and currency references
    cleanup_keywords = ['rupees', 'rs', 'add', 'at', 'for', 'expense', 'of', 'in', 'amount', 'on', 'spent']
    for word in cleanup_keywords:
        text = text.replace(word, '')

    # Remove special characters and digits
    text = re.sub(r'[^a-z\s]', '', text)
    category_words = text.strip().split()
    category = category_words[-1] if category_words else "other"

    return category, amount

def recognize_and_store_expense():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your expense (e.g., 'Add groceries for 500 rupees'):")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"📝 You said: {text}")

        category, amount = extract_expense(text)

        if amount > 0:
            save_to_db(category, amount)
            print(f"✅ Saved: {category} - ₹{amount}")
        else:
            print("⚠️ No valid amount found.")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"🔌 Could not request results; {e}")

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("📝 You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"🔌 Could not request results; {e}")
        return ""

if __name__ == "__main__":
    recognize_and_store_expense()
