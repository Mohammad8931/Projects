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
    
        
    # Some customers like 9467115 had NaN values in tx_count_30d/60d/90d.
    # After checking, this happened because they had no transactions in those time windows before the cutoff date.
    # To fix this, I replaced NaNs with 0 — it just means the customer was inactive during that time,
    # which is useful info for the model.
    for days in windows:
        df[f'tx_count_{days}d'] = df[f'tx_count_{days}d'].fillna(0).astype(int)

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

def avg_days_between_tx(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    data = data[data['date'] <= cutoff]

    # Sort and compute time gaps
    data = data.sort_values(['customer_id', 'date'])
    data['days_since_prev'] = data.groupby('customer_id')['date'].diff().dt.days

    # Average gap between transactions
    avg_gap = data.groupby('customer_id')['days_since_prev'].mean().reset_index()
    avg_gap.columns = ['customer_id', 'avg_days_between_tx']

    # Merge result back
    df = df.merge(avg_gap, on='customer_id', how='left')

    return df

def average_monthly_transactions(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Only include transactions before the cutoff date
    data = data[data['date'] <= cutoff]

    # Total transactions per customer
    txn_counts = data['customer_id'].value_counts().rename('total_txns')

    # First and last transaction dates
    first_txn = data.groupby('customer_id')['date'].min()
    last_txn = data.groupby('customer_id')['date'].max()

    customer_freq = pd.DataFrame({
        'total_txns': txn_counts,
        'first_date': first_txn,
        'last_date': last_txn
    })

    # Months active (at least 1 to avoid division by zero)
    customer_freq['months_active'] = ((customer_freq['last_date'] - customer_freq['first_date']) / pd.Timedelta(days=30)).clip(lower=1)
    # Average monthly transactions
    customer_freq['avg_monthly_txns'] = customer_freq['total_txns'] / customer_freq['months_active']
    # Merge with original dataframe
    df = df.merge(customer_freq[['avg_monthly_txns']], left_on='customer_id', right_index=True, how='left')

    return df

def add_target(df, cutoff_date='2019-01-31', prediction_window=90):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)
    end_date = cutoff + pd.Timedelta(days=prediction_window)

    # Filter future transactions in the prediction window
    future_tx = data[(data['date'] > cutoff) & (data['date'] <= end_date)]

    # Count transactions per customer in that window
    target = future_tx.groupby('customer_id').size().reset_index(name='target')

    # Merge target into original dataset
    df = df.merge(target, on='customer_id', how='left')
    df['target'] = df['target'].fillna(0).astype(int)

    return df

def reformat_df(df):
    data = df.copy()
    columns_to_drop = [
    'product_id', 'date', 'year', 'month', 'quarter',
    'year_month', 'year_quarter'
]
    data = data.drop(columns=columns_to_drop)
    data = data.drop_duplicates()

    return data




df = pd.read_csv('dataset/cleaned_dataset.csv')
df = recency(df)
df = count_transactions(df)
df = product_diversity(df)
df = avg_days_between_tx(df) 
df = average_monthly_transactions(df)
df = add_target(df)
# df.to_csv('dataset/feature_engineered_dataset.csv', index=False)
df = reformat_df(df)







# In the preprocessed dataset, we are still having some null values
# These belong to customers who had no transactions before the cutoff date — labeled as 'Inactive'.
# Since they have no historical behavior, key features like recency and transaction counts are missing (null).
# I calculated their percentage: they represent only 9.2% of all customers.
# I decided to remove them from the dataset because:
#   - We can't learn anything meaningful from their past behavior (it doesn’t exist).
#   - Including them would add noise and hurt the model’s ability to generalize.

def inactive_users(df):
    total = len(df)
    inactive = df[df['activity_level'] == 'Inactive'].shape[0]
    percent = (inactive / total) * 100
    print(f"{inactive} inactive customers ({percent:.1f}%) out of {total} total.")

print(inactive_users(df))


# delete inactive users 
df = df[df['activity_level'] != 'Inactive']


df.to_csv('dataset/preprocessed_dataset.csv', index=False)

