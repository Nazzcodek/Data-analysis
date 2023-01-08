# A D2B Assessment project
NB: The shipment_deliveries is the file name for the shipments_deliveries.csv file which was stated wrongly in the brief 

# ETL data analysis using Python and PostgreSQL
### Resources 
- Bucket Name: d2b-internal-assessment-bucket
- Data Locations: s3://d2b-internal-assessment-bucket/orders_data/*
- Database HOST	d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com
- DB_NAME	d2b_assessment

This project uses the ETL (extract, transform, load) model for data analysis. Three CSV files are imported using the Python boto3 library from an AWS S3 bucket and saved into a folder named [import_files](https://github.com/Nazzcodek/assesment/tree/main/import_files). The saved CSV files are then loaded into a PostgreSQL database in a schema specific to user nasibell8682_staging.

- `orders.csv`: A fact table that contains information about orders placed by customers, including the `order_id`, `customer_id`, `order_date`, `product_id`, `unit_price`, `quantity`, and `amount`
- `reviews.csv`: A fact table that contains customer reviews for products, including the `review` and the `product_id` being reviewed.
- `shipments_deliveries.csv`: A fact table that contains information about shipments and deliveries for orders, including the `shipment_id`, `order_id`, `shipment_date`, and `delivery_date`.

The psycopg2 library is used to connect to the database and load the CSV files into the database by creating a table for each file.

The database also has another schema named if_common that has four tables namely;
- `dim_customers`: A dimension table that contains information about customers, such as their `customer_id`, `customer_name`, and `postal_code`.
- dim_dates: a dimension table that contains information about dates, such as the `calendar_dt`, `year_num`, `month_of_the_year_num`, `day_of_the_month_num`, `day_of_the_week_num`, and `working_day fields`.
- `dim_addresses`: A dimension table that contains information about addresses, such as the `country`, `region`, `state`, and `address`
- `dim_product`: A dimension table that contains information about products, such as their `product_id`, `product_category`, and `product_name`.

if_common schema table used together with nasibell8682_staging schema table for transformation. Using SQL queries, three tables are created and filled with data from the queries, and these tables are saved in a schema named nasibell8682_analytics. The tables in nasibell8682_analytics are then exported into an S3 bucket as CSV files.

The repository contains the following files:

- `main.py`: Handles the extraction from the S3 bucket and loading to PostgreSQL.
- `main.tf`: Deploys export.py to export the files.
- `export.py`: Handles the exporting of the tables from nasibell8682_analytics to the S3 bucket.
- `scripts.sql`: Contains the SQL queries used for transformation.
- `requirements.txt`: Lists the dependencies for the project.

To run this project, you will need to have the following installed:

- Python
- PostgreSQL
- Terraform
The dependencies listed in requirements.txt

### To run the project, I used the following steps:

1. Set up my AWS account and PostgreSQL database.
2. Install the dependencies using `pip install -r requirements.txt`.
3. run `Makefile` to lint and format the `.py` extension files
3. Run `main.py` to extract the CSV files from the S3 bucket and load them into the `nasibell8682_staging` schema in PostgreSQL.
4. Run the SQL queries in `scripts.sql` to transform the data and create the tables in the `nasibell8682_analytics` schema.
5. Deploy `export.py` using `main.tf` to export the tables in `nasibell_analytics` to the S3 bucket.
