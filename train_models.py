import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import joblib

train = pd.read_csv('dataset/train_data.csv')
test = pd.read_csv('dataset/test_data.csv')

excluded_columns = ['customer_id', 'target']
X_train = train.drop(columns=excluded_columns)
y_train = train['target']
X_test = test.drop(columns=excluded_columns)
y_test = test['target']

# Scale features for linear models and XGBoost
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Trying different models and hyperparameters
models = {
    'Ridge': {
        'model': Ridge(),
        'params': {
            'alpha': [0.01, 0.1, 1.0, 10.0, 50.0, 100.0]
        },
        'scaled': True
    },
    'RandomForest': {
        'model': RandomForestRegressor(random_state=42),
        'params': {
            'n_estimators': [100, 200],
            'max_depth': [5, 10, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        },
        'scaled': False
    },
    'XGBoost': {
        'model': XGBRegressor(objective='reg:squarederror', random_state=42),
        'params': {
            'n_estimators': [100, 200],
            'max_depth': [3, 5],
            'learning_rate': [0.01, 0.05, 0.1]
        },
        'scaled': True
    }

}

best_model = None
best_r2 = -np.inf
best_name = ""

for name, cfg in models.items():
    X_tr = X_train_scaled if cfg['scaled'] else X_train
    X_te = X_test_scaled if cfg['scaled'] else X_test

    grid = GridSearchCV(
        cfg['model'],
        cfg['params'],
        scoring='r2',
        cv=5,
        n_jobs=-1
    )
    grid.fit(X_tr, y_train)

    # Predictions
    y_pred_train = grid.predict(X_tr)
    y_pred_test = grid.predict(X_te)

    # R² Scores
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)

    print(f"{name} | Train R²: {r2_train:} | Test R²: {r2_test}")

    if r2_test > best_r2:
        best_model = grid.best_estimator_
        best_r2 = r2_test
        best_name = name

joblib.dump(best_model, 'trained_models/best_model.joblib')
joblib.dump(scaler, 'trained_models/scaler.joblib')
print(f"\nBest model: {best_name}, Test R² = {best_r2}")
