import pandas as pd
import joblib
from sklearn.metrics import r2_score, root_mean_squared_error


model = joblib.load('trained_models/best_model.joblib')
scaler = joblib.load('trained_models/scaler.joblib')

test = pd.read_csv('dataset/test_data.csv')

customer_ids = test['customer_id']

X_test = test.drop(columns=['customer_id', 'target'])
y_test = test['target']

X_test_scaled = scaler.transform(X_test)

y_pred = model.predict(X_test_scaled)

# Evaluate
r2 = r2_score(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

# Display evaluation metrics
print("Evaluation Metrics on Test Set:")
print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

# Save predictions for review
results = pd.DataFrame({
    'customer_id': customer_ids,
    'actual': y_test,
    'predicted': y_pred
})
results.to_csv('predictions.csv', index=False)
print("\nPredictions saved to 'predictions.csv'")
