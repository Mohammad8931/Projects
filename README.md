# Customer Transaction Prediction System

This project predicts how many transactions each customer will make in the next 3 months based on their purchase history. I built it to help businesses understand customer behavior patterns and make better inventory and marketing decisions.

**The final model achieved 71.34% prediction accuracy using XGBoost after extensive feature engineering.**

## What This Project Does

Given transaction data (customer ID, product, timestamp), the system:

- Analyzes each customer's purchasing patterns
- Creates meaningful features from raw transaction data
- Trains multiple machine learning models to find the best predictor
- Saves predictions to a database for business use
- Provides a web interface for easy access to predictions

The main challenge was turning simple transaction records into rich customer profiles that capture buying behavior.

## How I Built It
    ├── EDA.ipynb # Comprehensive exploratory data analysis
    ├── train_models.py # Model training pipeline, used to train models, try different parameters and save the model 
    ├── evaluate_models.py # used to load the model and save predictions in prediction.csv and in MYSQL database.
    ├── model_utils.py # this file is where we created all the features used for making prediction(feature engineering), reformating dataset and adding target  
    ├── database_utils.py # used to connect to database and save predictions
    ├── api.py # Flask API to serve predictions from database
    ├── UI.py # Streamlit dashboard for viewing predictions
    ├── requirements.txt # Python dependencies
    ├── dataset/ # it contain many files, transactions_1.csv and transactions_2.csv are the raw data, cleaned_dataset.csv this the dataset after doing some cleaning in the EDA, train.csv and test.csv are generated in model_utils, they will be used directly in modelling part
    ├── trained_models/ # Saved model artifacts
    └── README.md # This file

## Tech Stack

I chose these tools for specific reasons:

- **Python** - Obviously, for data science work
- **scikit-learn** - Solid, reliable ML algorithms
- **XGBoost** - Best performance for this type of tabular data
- **pandas** - Makes data manipulation actually enjoyable
- **MySQL** - Store predictions for production use
- **joblib** - Fast model serialization
- **Flask** - Simple API for accessing predictions
- **Streamlit** - Quick web dashboard for viewing results

## Getting Started

**Setup:**

1. Clone this repo
2. Install requirements: `pip install -r requirements.txt`

## The Feature Engineering 

This is where I spent most of my time, and honestly, it was the most interesting part. Started with just basic stuff and kept adding features until the model stopped improving.
Features I added includes:

**Time-based Features:**

How many days since their last purchase (super important!)
Transaction counts in last 30/60/90 days
Average days between their purchases
Are they shopping more or less lately? (trend analysis)

**Shopping behavior:**

How many different products do they buy?
Do they stick to favorites or try new stuff?
How active are they compared to other customers? (Low/Medium/High tiers)
Recent activity score that weighs newer purchases more

**Product patterns:**

Ratio of unique products to total purchases (diversity)
How much they stick to their favorite product

and other features

## Model Training Results

I tested three different approaches:

Ridge         | Train R²: 0.5930 | Test R²: 0.5562
RandomForest  | Train R²: 0.8157 | Test R²: 0.6188
XGBoost       | Train R²: 0.8979 | Test R²: 0.7134
Winner: XGBoost with 71.34% accuracy

**Why XGBoost won:**
- Ridge was too simple for the complex customer patterns
- Random Forest overfitted (see that big gap between train/test scores?)
- XGBoost was complex enough to capture patterns, but didn't overfit

The 71% accuracy means the model explains about 71% of the variance in customer behavior - pretty solid for predicting human behavior!

## Running Predictions

**Train the models:**
```bash
python train_models.py
```

**Generate predictions:**
```bash
python evaluate_models.py
```

**View predictions in web dashboard:**
```bash
# Start the API
python api.py

# In another terminal, start the dashboard
streamlit run UI.py
```

The evaluation script loads the best model (XGBoost), processes your test data through the same feature pipeline, and outputs predictions with a performance report. The web dashboard provides an easy way to view all predictions without running scripts.

## Data Augmentation 

Since the dataset was small, I tried to expand it. instead of just one training cutoff date, I used multiple historical cutoffs (2017-11-30, 2018-11-30) to create more training examples. This gave the model more patterns to learn from. more cutoffs caused the models to memorize the training data instead of learning patterns in it, so i used only 2 cutoff's

## Database Integration

Predictions automatically get saved to MySQL in this format:

```sql
CREATE TABLE predictions_db (
    customer_id INT,
    cuttoff_date DATE,
    predicted INT,
    actual INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Customizing the System

**Change the prediction window:**
In `model_utils.py`, modify:
```python
def add_target(df, cutoff_date='2019-01-31', prediction_window=90):
    # Change 90 to whatever days you want to predict
```

**Change the main cutoff date:**
In `model_utils.py`, modify:
```python
cuttoff_date = '2019-01-31'  # Change to your desired cutoff date
```
This will automatically update training cutoffs and test predictions.

**Add new features:**
Create a new function in `model_utils.py` and add it to the `generate_features()` pipeline. The system will automatically include it in training.

**Try different models:**
Add them to the `models` dictionary in `train_models.py`. The training script will test them and pick the best one.

## Key Findings

Building this taught me a lot about customer behavior modeling:

1. **Feature engineering matters more than model choice** - Spent way more time on features than models
2. **Simple metrics can be powerful** - Basic recency and frequency patterns were surprisingly predictive
3. **Data augmentation helps** - Using multiple time cutoffs really improved performance
4. **No seasonality detected** - Ran visual analysis and ANOVA tests, found no significant seasonal patterns in the data

## Common Issues & Solutions

- **Missing transaction counts:** Filled with 0 (means customer was inactive)
- **Single-transaction customers:** Used cutoff date to estimate their typical gap
- **Inactive customers:** Filtered out during training (can't predict what we can't learn)

## Future Improvements

- Add customer segmentation visualization
- Implement prediction confidence intervals
- Create automated retraining pipeline
- Add model performance monitoring

## Some ideas I'd love to explore:
  - Visual components (charts showing customer segments)
  - File upload functionality



