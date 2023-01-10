# Configure the AWS provider
provider "aws" {
  access_key = "${ secrets.AWS_ACCESS_KEY_ID }"
  secret_key = "${ secrets.AWS_SECRET_ACCESS_KEY }"
  region     = "eu-central-1"
}


# zipping the export.py python file
data "archive_file" "zip_the_exportpy_code" {
type        = "zip"
source_file = "${path.module}/export.py" 
output_path = "export.zip"
}


# Create a Lambda function to run the export script
resource "aws_lambda_function" "export_function" {
  filename         = "export.zip" 
  function_name    = "export_table_to_s3"
  role             = "arn:aws:iam::711328479423:role/lambda_export_role"
  handler          = "export.export_table_to_s3"
  runtime          = "python3.9"

    environment {
    variables = {
      "RDS_HOST"     = "d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com",
      "RDS_USER"     = "nasibell8682",
      "RDS_PASSWORD" = "kBVtydZRpe",
      "RDS_DATABASE" = "d2b_assessment",
      "S3_BUCKET"    = "d2b-internal-assessment-bucket"
    }
  }
}
