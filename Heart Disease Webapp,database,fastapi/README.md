
# Heart Disease Classifier Project

## Introduction
This project utilizes machine learning to predict heart disease. 
It features a Streamlit web app for user interactions, Airflow for data ingestion, and a FastAPI server for backend operations.

## Project Structure
- `dags_ingestion_file.py`: Airflow DAG for data ingestion.
- `webapp.py`: Streamlit application for predictions.
- `db.py`: Sets up the PostgreSQL database schema.
- `api.py`: FastAPI server for prediction management.
- `errors_and_splitting.py`: Prepares and processes data.
- `model-industrialization-*.ipynb`: Jupyter notebooks for model development.
- `test.csv`: Sample dataset for demonstration.

## Installation
1. Environment Setup: install Docker, Docker Compose, and Python.
2. Clone the Project
3. Install Dependencies: `pip install -r requirements.txt`.
4. Database Setup: Run PostgreSQL, create `heart_disease_database`, and run `db.py`.
5. Start FastAPI Server: `uvicorn api:app --reload`.
6. Launch Streamlit Web App: `streamlit run webapp.py`.
7. Airflow Configuration: Adjust Docker Compose for Airflow, place `dags_ingestion_file.py` in Airflow's DAGs directory, and initialize the Airflow environment.

## Features
- Streamlit Web Application: Enables single and batch predictions. Saved predictions are stored in a database.
- Past Predictions Page: Users can query past predictions within a specified date range.
