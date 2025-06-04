from flask import Flask, jsonify
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/predictions')
def get_predictions():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    df = pd.read_sql("SELECT customer_id, cuttoff_date, predicted, actual FROM predictions_db", conn)
    conn.close()
    return jsonify(df.to_dict('records'))

app.run(port=5000) 