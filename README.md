# Automating S3 with Lambda Hands-On Lab

This project demonstrates how to automate the validation and management of CSV files uploaded to an Amazon S3 bucket using an AWS Lambda function written in Python. The Lambda function checks each row of the uploaded CSV for data quality and moves files with errors to a designated error bucket.

## Features

- **Automatic S3 Trigger:** Lambda is triggered when a new CSV file is uploaded to the billing bucket.
- **Row Validation:** Each row is checked for:
  - Valid product lines (`Bakery`, `Meat`, `Dairy`)
  - Valid currencies (`USD`, `MXN`, `CAD`)
  - Non-negative bill amounts
  - Correct date format (`YYYY-MM-DD`)
- **Error Handling:** If any row fails validation, the file is moved to an error bucket and deleted from the original bucket.
- **Logging:** Prints detailed error messages for invalid rows.

## Directory Structure

```
Automating_S3_with_Lambda_HOL/
│
├── BillingBucketParser/
│   ├── lambda_function.py   # Main Lambda handler and logic
│   └── event.json           # Sample event for local testing (if present)
|   └── template.yaml        # Defines Lambda function
├── README.md                # This file
```

## Getting Started

### Prerequisites

- AWS account with S3 and Lambda permissions
- Python 3.12
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library
- AWS SAM CLI (for local testing)

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/<repo-name>.git
    cd Automating_S3_with_Lambda_HOL
    ```

2. **Install dependencies:**
    ```bash
    pip install boto3
    ```

3. **Deploy the Lambda function using AWS SAM or manually upload the code to AWS Lambda.**
   AWS Toolkit --> Upload Lambda

### Local Testing

You can test the Lambda function locally using AWS SAM:

```bash
sam local invoke -e event.json
```

Where `event.json` is a sample S3 event.

## Lambda Function Overview

The Lambda function (`BillingBucketParser/lambda_function.py`) performs the following steps:

1. Downloads the uploaded CSV file from the S3 bucket.
2. Validates each row for product line, currency, bill amount, and date format.
3. If any row is invalid, moves the file to the error bucket and deletes it from the original bucket.
4. Logs errors and returns a status message.

## Example CSV Row

A valid row should look like:

```
...,Bakery,...,2025-07-15,USD,100.00,...
```

## Permissions

Ensure your Lambda execution role has the following S3 permissions for both the billing and error buckets:

- `s3:GetObject`
- `s3:PutObject`
- `s3:DeleteObject`
- `s3:CopyObject`

## License

MIT License

---

**Note:**  
This project is intended for educational purposes as part of a hands-on lab for automating S3 workflows
