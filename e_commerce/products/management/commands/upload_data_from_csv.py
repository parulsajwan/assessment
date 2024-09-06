import pandas as pd
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from products.models import Product
from products.helopers import data_cleaning


class Command(BaseCommand):
    '''
    Custom Django management command to upload product data from a CSV file into the database.
    Checks for the existence of the CSV file, reads and cleans the data, and updates or creates Product objects in the database based on the CSV content.
    '''
    help = 'Upload product data from a CSV file into the database'
    csv_path = Path(__file__).parent / "data.csv"

    def handle(self, *args, **kwargs):
        csv_file_path = self.csv_path

        if not os.path.exists(csv_file_path):
            raise CommandError(f"The file {csv_file_path} does not exist.")

        try:
            df = pd.read_csv(csv_file_path)
            df = data_cleaning(df)

        except Exception as e:
            raise CommandError(f"Error reading CSV file: {e}")

        required_columns = ['product_id', 'product_name', 'category',
                            'price', 'quantity_sold', 'rating', 'review_count']
        if not all(col in df.columns for col in required_columns):
            raise CommandError(
                f"Columns not found: {', '.join(required_columns)}")

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
