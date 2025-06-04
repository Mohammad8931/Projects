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

    # Some customers only made one purchase before the cutoff, so there's no previous transaction to compute an average gap.
    # For those users, we estimate the gap as the number of days between their only transaction and the cutoff date.
    single_tx_customers = avg_gap[avg_gap['avg_days_between_tx'].isna()]['customer_id']
    for customer_id in single_tx_customers:
        tx_date = data[data['customer_id'] == customer_id]['date'].iloc[0]
        days_since = (cutoff - tx_date).days
        avg_gap.loc[avg_gap['customer_id'] == customer_id, 'avg_days_between_tx'] = days_since
        
    # Merge result back
    df = df.merge(avg_gap, on='customer_id', how='left')

    return df



def assign_customer_tier(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Only use transactions before cutoff date
    data = data[data['date'] <= cutoff]

    # Count number of transactions per customer
    tx_counts = data['customer_id'].value_counts().reset_index()
    tx_counts.columns = ['customer_id', 'transaction_count']

    # Define activity thresholds
    high_threshold = tx_counts['transaction_count'].quantile(0.75)
    low_threshold = tx_counts['transaction_count'].quantile(0.25)

    def get_tier(txn):
        if txn >= high_threshold:
            return 'High'
        elif txn >= low_threshold:
            return 'Medium'
        else:
            return 'Low'
    tx_counts['activity_level'] = tx_counts['transaction_count'].apply(get_tier)

    # Merge into original dataframe
    df = df.merge(tx_counts[['customer_id', 'activity_level']], on='customer_id', how='left')
    df['activity_level'] = df['activity_level'].fillna('Inactive')
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

def tx_trend_60(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Define two 30-day windows
    recent_start = cutoff - pd.Timedelta(days=30)
    prev_start = cutoff - pd.Timedelta(days=60)
    
    recent_tx = data[(data['date'] > recent_start) & (data['date'] <= cutoff)]
    prev_tx = data[(data['date'] > prev_start) & (data['date'] <= recent_start)]
    
    recent_count = recent_tx.groupby('customer_id').size().reset_index(name='tx_last_30')
    prev_count = prev_tx.groupby('customer_id').size().reset_index(name='tx_prev_30')
    
    trend = pd.merge(recent_count, prev_count, on='customer_id', how='outer').fillna(0)
    trend['tx_trend_60'] = trend['tx_last_30'] - trend['tx_prev_30']
    
    df = df.merge(trend[['customer_id', 'tx_trend_60']], on='customer_id', how='left')
    df['tx_trend_60'] = df['tx_trend_60'].fillna(0).astype(int)
    
    return df

def tx_trend_90(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Last 30 days
    recent_start = cutoff - pd.Timedelta(days=30)
    prev_start = cutoff - pd.Timedelta(days=90)

    recent_tx = data[(data['date'] > recent_start) & (data['date'] <= cutoff)]
    prev_tx = data[(data['date'] > prev_start) & (data['date'] <= recent_start)]

    recent_count = recent_tx.groupby('customer_id').size().reset_index(name='tx_last_30')
    prev_count = prev_tx.groupby('customer_id').size().reset_index(name='tx_prev_60')

    trend = pd.merge(recent_count, prev_count, on='customer_id', how='outer').fillna(0)
    trend['tx_trend_90'] = trend['tx_last_30'] - (trend['tx_prev_60'] / 2)  # normalize per 30d

    df = df.merge(trend[['customer_id', 'tx_trend_90']], on='customer_id', how='left')
    df['tx_trend_90'] = df['tx_trend_90'].fillna(0)
    
    return df

def recent_activity_score(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    data = data[data['date'] <= cutoff]
    data['days_ago'] = (cutoff - data['date']).dt.days

    # Score: recent = high score (e.g., 1 / (1 + days_ago))
    data['recency_score'] = 1 / (1 + data['days_ago'])

    scores = data.groupby('customer_id')['recency_score'].sum().reset_index()
    scores.columns = ['customer_id', 'recent_activity_score']

    df = df.merge(scores, on='customer_id', how='left')
    df['recent_activity_score'] = df['recent_activity_score'].fillna(0)

    return df

def product_ratios(df, cutoff_date='2019-01-31'):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'], format='mixed', utc=True)
    cutoff = pd.to_datetime(cutoff_date, utc=True)

    # Only keep transactions before cutoff
    data = data[data['date'] <= cutoff]

    # Total transactions per customer
    total_tx = data.groupby('customer_id').size().reset_index(name='total_txns')

    # Number of unique products
    unique_products = data.groupby('customer_id')['product_id'].nunique().reset_index(name='num_unique_products')

    # Merge both
    merged = pd.merge(total_tx, unique_products, on='customer_id', how='outer')

    # Compute diversity ratio
    merged['product_diversity_ratio'] = merged['num_unique_products'] / merged['total_txns'].clip(lower=1)

    # Favorite product count per customer
    fav_counts = data.groupby(['customer_id', 'product_id']).size().reset_index(name='count')
    fav_max = fav_counts.sort_values(['customer_id', 'count'], ascending=[True, False]) \
                        .groupby('customer_id').first().reset_index()
    fav_max = fav_max[['customer_id', 'count']].rename(columns={'count': 'fav_product_count'})

    # Merge favorite count and compute ratio
    merged = pd.merge(merged, fav_max, on='customer_id', how='left')
    merged['favorite_product_ratio'] = merged['fav_product_count'] / merged['total_txns'].clip(lower=1)

    # Merge final results into main df
    df = df.merge(merged[['customer_id', 'product_diversity_ratio', 'favorite_product_ratio']],
                  on='customer_id', how='left')

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


def encode_categorical_features(df):
    data = df.copy()
    # due to the type of categorical data that we have(ordinal data), i preferred label encoding over one hot encoding
    activity_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    data['activity_level'] = data['activity_level'].map(activity_mapping)
    
    return data

def generate_features(df, cutoff_date):
    df = recency(df, cutoff_date)
    df = count_transactions(df, cutoff_date)
    df = product_diversity(df, cutoff_date)
    df = product_ratios(df, cutoff_date)
    df = avg_days_between_tx(df, cutoff_date)
    df = average_monthly_transactions(df, cutoff_date)
    df = assign_customer_tier(df, cutoff_date)
    df = tx_trend_60(df, cutoff_date)
    df = tx_trend_90(df, cutoff_date)
    df = recent_activity_score(df, cutoff_date)
    df = add_target(df, cutoff_date)
    df = df[df['activity_level'] != 'Inactive']
    df = encode_categorical_features(df)
    df = reformat_df(df)
    return df

def build_dataset(raw_df, cutoffs):
    return pd.concat([generate_features(raw_df.copy(), c) for c in cutoffs], ignore_index=True)



cuttoff_date = '2019-01-31'

#Since the dataset is small, i will do some data augmentation, by using different cuttoffs before 2019, and add them to the dataset
main_date = pd.to_datetime(cuttoff_date)

# We use 2 training periods from 2018 and 2017 to create more training examples
# These dates are far enough from our test period (Feb-May 2019) to avoid data leakage
# This way the model learns from past patterns without seeing future data
cutoffs = [
    (main_date - pd.DateOffset(months=14)).strftime('%Y-%m-%d'), 
    (main_date - pd.DateOffset(months=2)).strftime('%Y-%m-%d')   
]


raw_df = pd.read_csv('dataset/cleaned_dataset.csv')
train = build_dataset(raw_df, cutoffs)
train.to_csv('dataset/train_data.csv', index=False)

# we are trying to predict the number of transactions, 3 months after the  cuttoff_date ---> (for march, february and april 2019
test = generate_features(raw_df.copy(), cuttoff_date)
test.to_csv('dataset/test_data.csv', index=False)