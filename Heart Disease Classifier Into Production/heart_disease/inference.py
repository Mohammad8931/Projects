import joblib
import pandas as pd
from preprocess import preprocess

def make_predictions(data):
    data = data[selected_features]
    Scaler = joblib.load('../models/scaler.joblib')

    data_preprocessed,_ = scaling_features(data, is_train=False, scaler=Scaler)
    
    model = joblib.load('../models/model.joblib')
    prediction = model.predict(data_preprocessed)
    return pd.DataFrame(prediction, columns=['Prediction']).astype(int)

