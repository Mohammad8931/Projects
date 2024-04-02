import pandas as pd
import streamlit as st
import requests
from datetime import datetime

def show_predict_page():
    st.title('Heart Disease Prediction')
    st.subheader("Predict")

    st.write("Fill in the features for a single sample prediction:")
    thalach = st.text_input('thalach (maximum heart rate achieved)')
    cp = st.text_input('cp (chest pain type)')
    ca = st.text_input('ca (number of major vessels colored by flourosopy)')
    thal = st.text_input('thal (3 = normal; 6 = fixed defect; 7 = reversible defect)')
    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])

    st.write("\nOr upload a CSV file containing inference data (without labels):")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded data:")
        st.write(df)

    if st.button('Predict'):
        payload = {
            'thalach': thalach,
            'cp': cp,
            'ca': ca,
            'thal': thal,
            'prediction_source': "webapp"
        }

        if uploaded_file is None:
            response = requests.post('http://localhost:8000/predict', json=payload)
            if response.status_code == 200:
                prediction_result = response.json()
                st.subheader("Prediction Result")
                st.write("Prediction: ", prediction_result['result'])
                st.write("Features used:")
                for key, value in payload.items():
                    st.write(f"{key}: {value}")
            else:
                st.error("Failed to make prediction.")

        else:
            for index, row in df.iterrows():
                payload = {
                    'thalach': row['thalach'],
                    'cp': row['cp'],
                    'ca': row['ca'],
                    'thal': row['thal'],
                    'prediction_source': "webapp"
                }
                response = requests.post('http://localhost:8000/predict', json=payload)
                if response.status_code == 200:
                    prediction_result = response.json()
                    st.subheader(f"Prediction Result - Row {index + 1}")
                    st.write("Prediction: ", prediction_result['result'])
                    st.write("Features used:")
                    for key, value in payload.items():
                        st.write(f"{key}: {value}")
                else:
                    st.error(f"Failed to make prediction for Row {index + 1}.")

def show_past_predictions_page():
    st.title('Past Predictions')
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())
    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])

    if st.button("Fetch Past Predictions"):
        payload = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'prediction_source': prediction_source
        }
        response = requests.get('http://localhost:8000/past-predictions', params=payload)
        past_predictions = response.json()
        if past_predictions:
            st.subheader("Saved Predictions")
            for prediction in past_predictions:
                st.write(f"Prediction ID: {prediction['id']}")
                prediction_date = datetime.strptime(prediction['prediction_date'], "%Y-%m-%dT%H:%M:%S.%f")
                formatted_date = prediction_date.strftime("%Y-%m-%d")
                formatted_time = prediction_date.strftime("%H:%M:%S")
                st.write(f"Prediction Date: {formatted_date}")
                st.write(f"Prediction Time: {formatted_time}")
                
                st.write(f"Prediction Result: {prediction['result']}")
                features = prediction.get('features', [])
                if features:
                    st.write("\nFeatures Used:")
                    features_df = pd.DataFrame(features)
                    st.write(features_df)
                else:
                    st.write("No features used.")
                st.write("---")
        else:
            st.write("No past predictions found for the selected criteria.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Predict", "Past Predictions"])

    if page == "Predict":
        show_predict_page()
    elif page == "Past Predictions":
        show_past_predictions_page()

if __name__ == "__main__":
    main()
