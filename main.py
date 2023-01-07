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
s3.download_file(bucket_name, "orders_data/orders.csv", "orders.csv")
s3.download_file(bucket_name, "orders_data/reviews.csv", "reviews.csv")
s3.download_file(bucket_name, "orders_data/shipment_deliveries.csv", "shipments_deliveries.csv")


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
        with open(staging_area_file, "r") as f:
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
            # values = ','.join(['%s' for _ in range(len(header))])
            # insert_query = f"INSERT INTO nasibell8682_staging.{table_name} ({','.join(header)})  VALUES ({values})"
            # cursor.executemany(insert_query, data)

        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as error:
        # Log error and handle exception
        logging.error(error)


# List of files to load
orders = "orders.csv"
reviews = "reviews.csv"
shipments_deliveries = "shipments_deliveries.csv"
files = [orders, reviews, shipments_deliveries]

# Iterate over the files and load each one
for file in files:
    load_data(file)
# load_data(orders)
# load_data(reviews)
# load_data(shipments_deliveries)

with open(orders, "r") as f:
    data = csv.reader(f)
    header_row = next(data)  # Read the header row

    primary_key_column = header_row[0]

table_name = os.path.splitext(os.path.basename(orders))[0]
print(table_name)
print(primary_key_column)