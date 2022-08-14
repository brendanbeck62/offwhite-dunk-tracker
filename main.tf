terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  backend "s3" {
    bucket         = "offwhite-dunk-tracker-remote-state"
    encrypt        = true
    dynamodb_table = "offwhite-dunk-tracker-remote-state-lock"
    key            = "terraform.tfstate"
    region         = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"
}


# S3 bucket to hold the zip payload
# Creates the bucket
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "${var.prefix}-lambda-bucket"

  force_destroy = true
}

resource "aws_s3_bucket_acl" "lambda_bucket_acl" {
  bucket = aws_s3_bucket.lambda_bucket.id
  acl    = "private"
}

data "archive_file" "lambda_payload" {
  type = "zip"

  source_dir  = "${path.module}/src"
  output_path = "${path.module}/app.zip"
}

# uploads to the bucket
resource "aws_s3_object" "lambda_bucket_payload" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "app.zip"
  source = data.archive_file.lambda_payload.output_path

  etag = filemd5(data.archive_file.lambda_payload.output_path)
}

# lambda function
resource "aws_lambda_function" "app" {
  function_name = var.prefix

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_bucket_payload.key

  #runtime = "nodejs16.x"
  runtime = "python3.8"
  handler = "app.lambda_handler"

  source_code_hash = data.archive_file.lambda_payload.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "lambda-logs" {
  name = "/aws/lambda/${aws_lambda_function.app.function_name}"

  retention_in_days = 30
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
