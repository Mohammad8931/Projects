import pandas as pd
from sklearn.preprocessing import StandardScaler


def preprocess(data, is_train, scaler=None):
    
    data = data[selected_features]
    
    if is_train:
        scaler = StandardScaler()
        scaler.fit(data)
        scaled_data = scaler.transform(data)

    else:
        if scaler is None:
            raise ValueError("A fitted scaler must be provided for scaling test data.")
        scaled_data = scaler.transform(data)
        
    scaled_data = pd.DataFrame(scaled_data, index=data.index)

    return scaled_data, scaler

