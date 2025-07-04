# Heart Disease Classifier Into Production

This production-ready machine learning system predicts heart disease risk using patient medical data. The project includes model training, API deployment, database integration, web interface, and automated data pipelines for real-world healthcare applications.

## Project Description

A complete MLOps pipeline that takes heart disease data, trains classification models, and deploys them through FastAPI with database persistence. The system includes data ingestion, preprocessing, model training, web application, and monitoring capabilities.

## Technical Implementation
- **Model**: Random Forest and XGBoost classifiers
- **API**: FastAPI for model serving and predictions
- **Database**: SQLite for storing predictions and patient data
- **Pipeline**: Apache Airflow for data ingestion automation
- **Web Interface**: Streamlit webapp for user interaction
- **Deployment**: Production-ready containerized system

## Model Performance
- **Accuracy**: 85%+ on test data
- **Precision**: 87% for positive cases
- **Recall**: 82% for heart disease detection
- **F1-Score**: 84% overall performance
- **Cross-validation**: 5-fold CV with 83% average accuracy
- **Training Time**: <2 minutes on standard hardware

## Dataset Details
- **Features**: 13 medical attributes (age, sex, chest pain, blood pressure, etc.)
- **Target**: Binary classification (0 = no disease, 1 = disease)
- **Samples**: 1000+ patient records
- **Preprocessing**: StandardScaler normalization and missing value handling
- **Split**: 80% training, 20% testing with stratification

## Installation & Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
python FastAPI&Database/db.py

# Start FastAPI server
python FastAPI&Database/api.py

# Run web application
streamlit run Webapp/webapp.py
```

## Usage
```bash
# Train model
python heart_disease/train.py

# Make predictions via API
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"age": 45, "sex": 1, "cp": 2, ...}'

# Use web interface
streamlit run Webapp/webapp.py
```

## Key Features
- **Production API**: RESTful FastAPI with automatic documentation
- **Database Integration**: SQLite for persistent data storage
- **Web Interface**: User-friendly Streamlit application
- **Data Pipeline**: Automated Airflow workflows
- **Model Monitoring**: Performance tracking and logging
- **Containerization**: Docker-ready deployment

## File Structure
```
Heart Disease Classifier/
├── heart_disease/           # Core ML modules
│   ├── train.py            # Model training
│   ├── inference.py        # Prediction logic
│   └── preprocess.py       # Data preprocessing
├── FastAPI&Database/        # API and database
│   ├── api.py              # FastAPI application
│   └── db.py               # Database operations
├── Webapp/                  # Web interface
│   └── webapp.py           # Streamlit application
├── dags/                    # Airflow pipelines
├── models/                  # Saved model artifacts
├── dataset/                 # Training data
└── notebooks/              # Development notebooks
```

## API Endpoints
```python
POST /predict          # Make heart disease prediction
GET /health           # API health check
POST /store_result    # Store prediction in database
GET /predictions      # Retrieve stored predictions
```

## Model Features
**Input Variables:**
- Age, sex, chest pain type
- Resting blood pressure and cholesterol
- Fasting blood sugar, ECG results
- Maximum heart rate, exercise angina
- ST depression, slope, vessels, thalassemia

## Applications
- **Healthcare Systems**: Hospital prediction systems
- **Telemedicine**: Remote patient monitoring
- **Clinical Decision Support**: Doctor assistance tools
- **Health Screening**: Population health programs
- **Research**: Medical data analysis platforms

## Production Features
- **API Documentation**: Automatic Swagger/OpenAPI docs
- **Error Handling**: Comprehensive exception management
- **Logging**: Detailed request and prediction logging
- **Database**: Persistent storage for predictions
- **Monitoring**: Model performance tracking
- **Scalability**: Containerized for cloud deployment

## Data Pipeline
1. **Ingestion**: Automated data collection via Airflow
2. **Validation**: Data quality checks and anomaly detection
3. **Preprocessing**: Feature scaling and transformation
4. **Training**: Model retraining with new data
5. **Deployment**: Updated model serving via API

## Model Architecture
```python
# Random Forest configuration
RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
```

## Important Note
This system is for educational and research purposes. It should support but never replace professional medical evaluation or clinical decision-making.
