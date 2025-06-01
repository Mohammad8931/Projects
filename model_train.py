import pandas as pd
from sklearn.model_selection import train_test_split


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

dataset = pd.read_csv('dataset/preprocessed_dataset.csv')
X, y = prepare_features_target(dataset)
X_train, X_test, y_train, y_test = split_data(X,y)
