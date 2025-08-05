import tkinter as tk
from tkinter import ttk
from voice.voice_input import get_voice_input
from voice.text_to_command import parse_command
import requests
import threading
import time

# GUI Setup
app = tk.Tk()
app.title("FinVoice - Voice Finance Tracker")
app.geometry("600x400")

label = tk.Label(app, text="🎤 Voice Assistant is Listening...", font=("Arial", 12))
label.pack(pady=10)

# Frame for messages and table
status_frame = tk.Frame(app)
status_frame.pack(pady=5, fill="both", expand=True)

status_label = tk.Label(status_frame, text="", wraplength=550, font=("Arial", 10), fg="blue", justify="left")
status_label.pack()

# Table setup
tree = ttk.Treeview(status_frame, columns=("Category", "Amount"), show="headings", height=10)
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount (₹)")
tree.column("Category", anchor=tk.W, width=200)
tree.column("Amount", anchor=tk.CENTER, width=100)

total_label = tk.Label(app, text="", font=("Arial", 11, "bold"), fg="green")

def update_status(message):
    status_label.config(text=message)
    tree.pack_forget()
    total_label.pack_forget()
    status_label.pack()

def show_expense_table(expenses):
    status_label.pack_forget()
    tree.delete(*tree.get_children())  # Clear old rows

    total = 0
    for e in expenses:
        category = e["category"]
        amount = e["amount"]
        tree.insert("", "end", values=(category, f"₹{amount:.2f}"))
        total += amount

    tree.pack(pady=5)
    total_label.config(text=f"🧮 Total: ₹{total:.2f}")
    total_label.pack()

def handle_voice():
    while True:
        try:
            text = get_voice_input()
            if not text:
                continue

            result = parse_command(text)

            if result["action"] == "add":
                res = requests.post("http://localhost:5000/add_expense", json=result)
                update_status(f"✅ Added ₹{result['amount']} to {result['category']}")

            elif result["action"] == "show":
                res = requests.get("http://localhost:5000/expenses")
                expenses = res.json()
                if expenses:
                    show_expense_table(expenses)
                else:
                    update_status("📭 No expenses recorded yet.")
                    tree.delete(*tree.get_children())
                    tree.pack_forget()
                    total_label.pack_forget()

            elif result["action"] == "delete_all":
                res = requests.post("http://localhost:5000/delete_all")
                update_status("🗑️ All expenses deleted.")
                tree.delete(*tree.get_children())
                tree.pack_forget()
                total_label.pack_forget()

            elif result["action"] == "exit":
                update_status("👋 Exiting app...")
                time.sleep(2)
                app.quit()
                break

            else:
                update_status("⚠️ Could not process command.")

        except Exception as e:
            print(f"Error: {e}")
            update_status(f"❌ Error: {e}")

        time.sleep(1)

# Background thread for voice input
threading.Thread(target=handle_voice, daemon=True).start()

app.mainloop()