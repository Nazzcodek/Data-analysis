[![Makefile CI](https://github.com/Nazzcodek/assesment/actions/workflows/makefile.yml/badge.svg)](https://github.com/Nazzcodek/assesment/actions/workflows/makefile.yml)
[![Terraform](https://github.com/Nazzcodek/assesment/actions/workflows/terraform.yml/badge.svg)](https://github.com/Nazzcodek/assesment/actions/workflows/terraform.yml)
# A D2B Assessment project
This project is an ETL data analysis using data engineering principles (CI/CD) that uses Python and PostgreSQL to extract, transform, and load data from CSV files in an AWS S3 bucket into a PostgreSQL database. The transformed data is then exported back to the S3 bucket as CSV files. 

For CI/CD Github action is used, Makefile is used for Continuous Integration of the codes while terraform for Continuous Delivery to meet DevOps best practice. 

# ETL data analysis using Python and PostgreSQL
### Resources 
- Bucket Name: d2b-internal-assessment-bucket
- Data Locations: s3://d2b-internal-assessment-bucket/orders_data/*
- Database HOST	d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com
- DB_NAME	d2b_assessment

This project uses the ETL (extract, transform, load) model for data analysis. Three CSV files are imported using the Python boto3 library from an AWS S3 bucket and saved into a folder named [import_files](https://github.com/Nazzcodek/assesment/tree/main/import_files). The saved CSV files are then loaded into a PostgreSQL database in a schema specific to user nasibell8682_staging.

NB: The shipment_deliveries is the file name for the shipments_deliveries.csv file which was stated wrongly in the brief 

- `orders.csv`: A fact table that contains information about orders placed by customers, including the `order_id`, `customer_id`, `order_date`, `product_id`, `unit_price`, `quantity`, and `amount`
- `reviews.csv`: A fact table that contains customer reviews for products, including the `review` and the `product_id` being reviewed.
- `shipments_deliveries.csv`: A fact table that contains information about shipments and deliveries for orders, including the `shipment_id`, `order_id`, `shipment_date`, and `delivery_date`.

The psycopg2 library is used to connect to the database and load the CSV files into the database by creating a table for each file.

The `if_common` schema contains four dimension tables that are used to enrich the data in the `nasibell8682_staging` schema during the transformation process. These tables are:

- `dim_customers`: Contains information about customers, such as their `customer_id`, `customer_name`, and `postal_code`.
- `dim_dates`: Contains information about dates, such as the `calendar_dt`, `year_num`, `month_of_the_year_num`, `day_of_the_month_num`, `day_of_the_week_num`, and `working_day` fields.
- `dim_addresses`: Contains information about addresses, such as the `country`, `region`, `state`, and `address`.
- `dim_product`: Contains information about products, such as their `product_id`, `product_category`, and `product_name`.

These dimension tables are used together with the fact tables in the `nasibell8682_staging` schema to create the transformed tables in the `nasibell8682_analytics` schema.


The repository contains the following files:

- `main.py`: Handles the extraction from the S3 bucket and loading to PostgreSQL.
- `main.tf`: Deploys export.py to export the files.
- `export.py`: Handles the exporting of the tables from nasibell8682_analytics to the S3 bucket.
- `scripts.sql`: Contains the SQL queries used for transformation.
- `requirements.txt`: Lists the dependencies for the project.
- `Makefile`: The `Makefile` in this project contains a set of commands that can be run to lint and format the `.py` extension files. To run the `Makefile`, use the command `make <target>`, where `<target>` is the name of the target you want to run. For example, to lint the `.py` extension files, you can use the command `make lint`.

To run this project, you will need to have the following installed:

- Python
- PostgreSQL
- Terraform
The dependencies listed in requirements.txt

### To run the project, I used the following steps:

1. Set up my AWS account and PostgreSQL database.
2. Install the dependencies using `pip install -r requirements.txt`.
3. run `Makefile` to lint and format the `.py` extension files for continuous integration CI
3. Run `main.py` to extract the CSV files from the S3 bucket and load them into the `nasibell8682_staging` schema in PostgreSQL.
4. Run the SQL queries in `scripts.sql` to transform the data and create the tables in the `nasibell8682_analytics` schema.
5. Deploy `export.py` using `main.tf` to export the tables in `nasibell8682_analytics` to the S3 bucket.

### Using Terraform
In `main.tf` the code doesn't include any provision for `IAM Role` or `Policy` which are requirements to successfuly provision using terraform, as a user with no permission to create a role or access any role within the organization AWS account, a personal account was used to create a role and added the required policy i.e `AmazonS3FullAccess` and `AmazonRDSFullAccess` to successful deploy using terraform. The ARN of the role created in the user's AWS account is what was used to create the lambda function used for the deployment.

To deploy using `main.tf` terraform file, three commands must be run using any CLI which are; 
- `terraform init` prepares the working directory so Terraform can run the configuration
- `terraform plan' lets you preview any changes before you apply them.
- `terraform apply` executes the changes defined by the Terraform configuration to create, update, or destroy resources.

Terraform was used to deploy the `export.py` while the `main.py` was deploy using CLI command `python main.py`


