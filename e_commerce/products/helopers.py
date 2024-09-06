import pandas as pd
from .models import Product


def upload_product_data(csv_file_path):
    '''
    Uploads product data from a CSV file to the database.

    Args:
        csv_file_path (str): The file path of the CSV file containing product data.

    Returns:
        None
    '''
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        Product.objects.update_or_create(
            product_id=row['product_id'],
            defaults={
                'product_name': row['product_name'],
                'category': row['category'],
                'price': row['price'],
                'quantity_sold': row['quantity_sold'],
                'rating': row['rating'],
                'review_count': row['review_count'],
            }
        )


def data_cleaning(df):
    '''
    Perform data cleaning on the input DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing columns 'price', 'quantity_sold', 'rating', 'review_count'.

    Returns:
    - pd.DataFrame: DataFrame with cleaned data after filling missing values and converting columns to numeric types.
    '''
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')

    df['price'].fillna(df['price'].median(), inplace=True)
    df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
    df['rating'] = df.groupby('category')['rating'].transform(
        lambda x: x.fillna(x.mean()))
    df['review_count'].fillna(0, inplace=True)

    return df
