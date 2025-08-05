import sqlite3
import pandas as pd

def generate_monthly_report():
    conn = sqlite3.connect("finvoice.db")
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%B')

    summary = df.groupby(['month', 'category'])['amount'].sum().unstack().fillna(0)
    print(summary)
    summary.to_excel("Monthly_Report.xlsx")
    conn.close()
