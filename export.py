import psycopg2
import csv
import boto3
from io import StringIO
import logging


def export_table_to_s3(table_name):
    try:
        # Connect to the database
        connection = psycopg2.connect(
            database='d2b_assessment',
            user='nasibell8682',
            password='kBVtydZRpe',
            host='d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com'
        )
        cursor = connection.cursor()

        # Execute a command to retrieve the data from the table
        cursor.execute(f"SELECT * FROM nasibell8682_analytics.{table_name}")

        # Fetch all the rows of the table
        rows = cursor.fetchall()

        # Generate the file name
        file_name = f"{table_name}.csv"

        # Create a new file on S3
        s3 = boto3.resource("s3")
        bucket = s3.Bucket("d2b-internal-assessment-bucket")
        objects = bucket.Object(f"/analytics_export/nasibell8682/{file_name}")

        # Write the rows to the file
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        for row in rows:
            writer.writerow(row)

        objects.put(Body=csv_buffer.getvalue())

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except psycopg2.OperationalError as error:
        # Log error and handle exception
        logging.error(error)

# export the tables
tables = ['best_performing_product', 'agg_public_holiday', 'agg_shipments']
for table in tables:
    export_table_to_s3(table)
