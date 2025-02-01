# Dummy Code to process the data and upload to GSC.
# Make sure Bucket exists. If not create it from Web Console.

import json
from datetime import datetime
from google.cloud import storage

BUCKET_NAME = "my-gcp-bucket-name"

def fetch_sales_data():
    """Simulate fetching sales data from a database."""
    print("Fetching Sales Data....")
    sales_data = [
        {"product": "Laptop", "quantity": 5, "total_price": 5000},
        {"product": "Headphone", "quantity": 5, "total_price": 1500},
        {"product": "Mobile", "quantity": 5, "total_price": 2500},
    ]

