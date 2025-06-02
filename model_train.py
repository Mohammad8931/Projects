import pandas as pd
from sklearn.model_selection import train_test_split
import time 
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.ensemble import RandomForestRegressor

def prepare_features_target(df):
    print(df.columns)
    # Remove customer_id as it's not a predictive feature
    target = df['target']
    features = df.drop(['target', 'customer_id'], axis=1)

    return features, target


def split_data(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    print(f"X train shape : {X_train.shape}") #(1453, 8)
    print(f"X test shape : {X_test.shape}") #(364, 8)
    print(f"y train shape : {y_train.shape}")  #(1453,)
    print(f"y test shape: {y_test.shape}") #(364,)
    
    return X_train, X_test, y_train, y_test

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):

    # Train the model
    model.fit(X_train, y_train)
    # Make predictions
    y_test_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_test_pred)
    
    r2_test = r2_score(y_test, y_test_pred)
    
    RMSE = root_mean_squared_error(y_test, y_test_pred)
    
    
    # i will computer training error and compare it with test error to check underfitting and overfitting
    y_train_pred = model.predict(X_train)
    r2_train = r2_score(y_train, y_train_pred)

    print(f"its MAE: {mae}, RMSE : {RMSE}, R² score: {r2_test}")
    print(f"Train R²: {r2_train}, Test R²: {r2_test}")

    return model




dataset = pd.read_csv('dataset/preprocessed_dataset.csv')
X, y = prepare_features_target(dataset)
X_train, X_test, y_train, y_test = split_data(X,y)
model = train_and_evaluate_model(RandomForestRegressor(n_estimators=300, max_depth=10,  min_samples_split=5, min_samples_leaf=2,random_state=42))





