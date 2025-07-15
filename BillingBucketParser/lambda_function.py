# Import necessary modules
# CSV for handling CSV files, boto3 for AWS SDK, datetime for date operations
import csv
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Initialize the s3 resource using boto3
    s3 = boto3.resource('s3')

    # Extract the bucket name and the CSV file name from the 'event' input
    billing_bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']

    # Define the name of the error bucket where you want to copy the erroneous CSV files
    error_bucket = 'dct-billing-errors-2025'

    # Download the CSV file from S3, read the content, decode from bytes to string, and split the content by lines
    obj = s3.Object(billing_bucket, csv_file)
    data = obj.get()['Body'].read().decode('utf-8').splitlines()

    # Initialize a flag (error_found) to false. We will set this flag to true when we find an error.
    error_found = False 

    # Define valid product lines and valid currencies
    valid_product_lines = ['Bakery', 'Meat', 'Dairy']
    valid_currencies = ['USD', 'MXN', 'CAD']

    # Read the CSV content line by line using Python's csv reader. Ignore the header line (data[1:])
    for row in csv.reader(data[1:], delimiter=','):
        # For each row, extract the product line, currency, amount, and date from the specific columns
        date = row[6]
        product_line = row[4]
        currency = row[7]
        bill_amount = float(row[8])

        # Check if the product line is valid. If not, set error_found to true and print an error message
        if product_line not in valid_product_lines:
            error_found = True
            print(f"Error in record {row[0]}: Product line '{product_line}' is not valid. Valid product lines are {valid_product_lines}.")
            break
        # Check if currency is valid. If not, set error_found to true and print an error message
        if currency not in valid_currencies:
            error_found = True
            print(f"Error in record {row[0]}: Currency '{currency}' is not valid. Valid currencies are {valid_currencies}.")
            break
        # Check if the bill amount is negative. If so, set error_found to true and print an error message
        if bill_amount < 0:
            error_found = True
            print(f"Error in record {row[0]}: Bill amount {bill_amount} is negative.")
            break
        # Check if the date is in the correct format (YYYY-MM-DD). If not, set error_found to true and print an error message
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_found = True
            print(f"Error in record {row[0]}: Date {date} is not in the correct format (YYYY-MM-DD).")
            break
    # After checking all rows, if error_found is true, copy the erroneous CSV file to the error bucket
    if error_found:
        copy_source = {
            'Bucket': billing_bucket,
            'Key': csv_file            
            }
        try:        
            s3.meta.client.copy(copy_source, error_bucket, csv_file)
            print(f"Moved errenous file to: {error_bucket}.") 
            s3.Object(billing_bucket, csv_file).delete()
            print("Deleted original file from bucket.")         
        # Handle any exception that may occur while moving the file, and print the error message
        except Exception as e:    
            print(f"Error while movie file: {str(e)}.") 
            
    # If no errors were found, return a success message with status code 200 and a body message indicating that no errors were found
    else:    
        return {
            'statusCode': 200,
            'body': 'No errors found in the CSV file!'
        }