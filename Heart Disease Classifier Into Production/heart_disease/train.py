import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from preprocess import preprocess
from constants import FEATURES, TARGET_COLUMN


def build_model(data: pd.DataFrame):
    y = data.loc[:, data.columns == 'target']
    X = data.loc[:, data.columns != 'target']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    x_train = x_train[selected_features]


    x_train_preprocessed,Scaler = scaling_features(x_train, is_train=True, scaler=None)
    x_test_preprocessed,_ = scaling_features(x_test, is_train=False, scaler=Scaler)
    model = LogisticRegression()

    model.fit(x_train_preprocessed, y_train)

    y_pred = model.predict(x_test_preprocessed)

    loss = compute_log_loss(y_test, y_pred)

    return {'loss': round(loss, 2)},model

