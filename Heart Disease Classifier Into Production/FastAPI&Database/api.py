from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Prediction, Feature, Base
from datetime import datetime
import joblib
import numpy as np

app = FastAPI()

# Load the model and scaler
MODEL_PATH = "../models/model.joblib"
SCALER_PATH = "../models/scaler.joblib"
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Create database connection
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/heart_disease_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class HeartDiseaseInput(BaseModel):
    thalach: float
    cp: float
    ca: float
    thal: float
    prediction_source: str

class PredictionResult(BaseModel):
    result: str

class PredictionWithFeatures(BaseModel):
    id: int
    prediction_date: datetime
    result: str
    features: list

# Endpoint to save new prediction
@app.post("/predict", response_model=PredictionResult)
def predict_disease(data: HeartDiseaseInput):
    db = SessionLocal()
    try:
        prediction_data = data.dict(exclude={'prediction_source'})
        scaled_features = scaler.transform([[data.thalach, data.cp, data.ca, data.thal]])
        prediction_result = model.predict(scaled_features)
        prediction_result_str = "High probability of heart disease." if prediction_result[0] == 1 else "Low probability of heart disease."
        prediction = Prediction(**prediction_data, result=prediction_result_str, prediction_date=datetime.now(), prediction_source=data.prediction_source)
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        features = [Feature(name=name, value=str(value), prediction_id=prediction.id) for name, value in prediction_data.items()]
        db.add_all(features)
        db.commit()

        return {"result": prediction_result_str}
    finally:
        db.close()

# Endpoint to retrieve past predictions
@app.get("/past-predictions")
def get_past_predictions(start_date: datetime, end_date: datetime, prediction_source: str):
    db = SessionLocal()
    try:
        if prediction_source == "all":
            past_predictions = db.query(Prediction).filter(
                Prediction.prediction_date >= start_date,
                Prediction.prediction_date <= end_date,
            ).all()
        else:
            past_predictions = db.query(Prediction).filter(
                Prediction.prediction_date >= start_date,
                Prediction.prediction_date <= end_date,
                Prediction.prediction_source == prediction_source
            ).all()

        past_predictions_with_features = []
        for prediction in past_predictions:
            features = db.query(Feature).filter(Feature.prediction_id == prediction.id).all()
            features_data = [{"name": feature.name, "value": feature.value} for feature in features]
            past_predictions_with_features.append({
                "id": prediction.id,
                "prediction_date": prediction.prediction_date,
                "result": prediction.result,
                "features": features_data
            })
        return past_predictions_with_features
    finally:
        db.close()
