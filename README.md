# 🧾 FinVoice

A voice-powered personal finance tracker built using Python (frontend + backend).

## Features

- Voice recognition for adding expenses
- Flask API to store and retrieve data
- Tkinter GUI for user interaction
- SQLite database
- PDF/Excel report generation

## How to Run

1. Install requirements:
   pip install -r requirements.txt

2. Start backend:
   PYTHONPATH=. python backend/app.py

3. Start frontend:
   npm start

4. Generate report (optional):
   PYTHONPATH=. python reports/report_generator.py
