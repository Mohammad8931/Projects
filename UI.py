import streamlit as st
import requests
import pandas as pd

st.title("Customer Predictions")

response = requests.get("http://localhost:5000/predictions")
data = pd.DataFrame(response.json())

st.write(f"Total Predictions: {len(data)}")
st.dataframe(data) 