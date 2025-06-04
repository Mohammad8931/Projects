import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def save_predictions(df):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions_db (
            customer_id INT,
            cuttoff_date DATE,
            predicted INT,
            actual INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO predictions_db (customer_id, cuttoff_date, predicted, actual) VALUES (%s, %s, %s, %s)",
            (str(row['customer_id']), row['cuttoff_date'], int(row['predicted']), int(row['actual']))
        )
    conn.commit()
    conn.close()