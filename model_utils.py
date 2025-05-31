import pandas as pd

def recency(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format = 'mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc = True)
    
    # Only keep transactions before cutoff date
    data = data[data['date'] <= cutoff]
    
    # Find each customer's most recent purchase date
    last_purchases = data.groupby('customer_id')['date'].max().reset_index()

    # Calculate days between cutoff date and last purchase
    last_purchases['days_since_last_purchase'] = (cutoff - last_purchases['date']).dt.days
    
    df = df.merge(
        last_purchases[['customer_id', 'days_since_last_purchase']],
        on='customer_id',
        how='left'
    )
    return df

def count_transactions(df, cutoff_date='2019-01-31', windows=[30, 60, 90]):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'],format = 'mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Initialize a DataFrame with unique customer IDs
    result = pd.DataFrame(data['customer_id'].unique(), columns=['customer_id'])

    # For each window, calculate number of transactions before cutoff
    for days in windows:
        start = cutoff - pd.Timedelta(days=days)
        mask = (data['date'] > start) & (data['date'] <= cutoff)
        tx = data[mask]
        tx_count = tx.groupby('customer_id').size().reset_index(name=f'tx_count_{days}d')
        result = result.merge(tx_count, on='customer_id', how='left')

    # Merge final results into the original dataset
    df = df.merge(result, on='customer_id', how='left')

    return df

def product_diversity(df, cutoff_date='2019-01-31'):
    
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)
    
    # Only keep transactions before cutoff date
    data = data[data['date'] <= cutoff]
    
    # Count unique products per customer
    diversity = data.groupby('customer_id')['product_id'].nunique().reset_index()
    diversity.columns = ['customer_id', 'num_unique_products']
    
    # Merge diversity counts into original dataset
    df = df.merge(diversity, on='customer_id', how='left')
    
    return df


df = pd.read_csv('dataset/cleaned_dataset.csv')
df = recency(df)
df = count_transactions(df)
df = product_diversity(df)
df.to_csv('dataset/feature_engineered_dataset.csv', index=False)