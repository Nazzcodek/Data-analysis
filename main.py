import logging
import psycopg2
import os
import csv

import boto3
from botocore import UNSIGNED
from botocore.client import Config

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
bucket_name = "d2b-internal-assessment-bucket"
response = s3.list_objects(Bucket=bucket_name, Prefix="orders_data")

# Extracting data from source
s3.download_file(bucket_name, "orders_data/orders.csv", "import_files/orders.csv")
s3.download_file(bucket_name, "orders_data/reviews.csv", "import_files/reviews.csv")
s3.download_file(bucket_name, "orders_data/shipment_deliveries.csv", "import_files/shipments_deliveries.csv")


# Load data from CSV files into PostgreSQL staging tables
def load_data(staging_area_file):
    try:
        # Connect to PostgreSQL staging database
        connection = psycopg2.connect(
            database='d2b_assessment',
            user='nasibell8682',
            password='kBVtydZRpe',
            host='d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com'
        )
        cursor = connection.cursor()

        # Get the file name and remove the extension
        table_name = os.path.splitext(os.path.basename(staging_area_file))[0]

        # Read data from the file
        with open(staging_area_file, "r",  encoding='utf-8') as f:
            data = csv.reader(f)
            header_row = next(data)  # Read the header row

            if table_name == "reviews":
                # Create a new table without a primary key
                column_defs = ",".join([f"{column} SERIAL" for column in header_row])
                create_table_query = f"CREATE TABLE nasibell8682_staging.{table_name} ({column_defs});"
            else:
                primary_key_column = header_row[0]

                # Create a new table statement
                column_defs = []
                for column in header_row[1:]:
                    if column.endswith("_date"):
                        column_defs.append(f"{column} date")
                    else:
                        column_defs.append(f"{column} SERIAL")
                column_defs = ",".join(column_defs)
                create_table_query = f"CREATE TABLE nasibell8682_staging.{table_name} ({primary_key_column} SERIAL PRIMARY KEY,  {column_defs});"

            # Delete the existing table if it exists
            cursor.execute(f"DROP TABLE IF EXISTS nasibell8682_staging.{table_name}")

            # create a new table to store the data
            cursor.execute(create_table_query)

            # Insert data into the staging table
            cursor.copy_expert(f"COPY nasibell8682_staging.{table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)", f)

        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()

    except psycopg2.OperationalError as error:
        # Log error and handle exception
        logging.error(error)


# List of files to load
orders = "import_files/orders.csv"
reviews = "import_files/reviews.csv"
shipments_deliveries = "import_files/shipments_deliveries.csv"
files = [orders, reviews, shipments_deliveries]

# Iterate over the files and load each one
for file in files:
    load_data(file)
