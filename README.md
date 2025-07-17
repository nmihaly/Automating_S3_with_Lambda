
```markdown
📂 Automating S3 with Lambda

A hands-on AWS Lambda project that validates `.csv` files uploaded to an S3 bucket. If the file fails validation, it's automatically moved to an error bucket for review — a simple and efficient serverless workflow for file validation pipelines.

---

🧠 Overview

This project demonstrates how to:

- Use AWS Lambda to process and validate `.csv` files
- Read S3 events to trigger Lambda functions
- Apply validation logic to file contents
- Move invalid files to a separate S3 error bucket
- Set up and test Lambda functions locally using SAM (Serverless Application Model)

---

📋 Features

- ✅ Validates product line, currency, bill amount, and date fields
- ⚙️ Built with Python 3.12 and Boto3
- ☁️ Runs on AWS Lambda, triggered by S3 events
- 🔄 Automatically deletes invalid files from the source bucket
- 🧪 Includes local testing setup using `sam local invoke`

---

📁 Folder Structure

.
├── lambda\_function.py      # Main Lambda code
├── template.yaml           # SAM template for local testing
├── event.json              # Sample S3 event trigger
├── test\_data/              # Sample CSV files for testing
└── README.md               # You're here

````

---

### 🚀 Getting Started

### 1. Prerequisites

- AWS CLI configured
- AWS Toolkit for VS Code (recommended)
- Python 3.12
- Docker (for local testing)
- SAM CLI

### 2. Clone the Repo

```bash
git clone https://github.com/nmihaly/Automating_S3_with_Lambda.git
cd Automating_S3_with_Lambda
````

### 3. Set Up Resources

Create two S3 buckets:

* `billing-2025` – upload bucket
* `billing-errors-2025` – error bucket

Upload a test `.csv` to the upload bucket before testing.

---

## 🧪 Local Testing (SAM)

### Edit `event.json` with your S3 bucket and file name:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "billing-2025" },
        "object": { "key": "billing_data_meat_may_2023.csv" }
      }
    }
  ]
}
```

### Run the test:

```bash
sam local invoke -e event.json
```

Expected output (if validation fails):

```
Error in record 11: Date 5/11/2023 is not in the correct format (YYYY-MM-DD).
Moved erroneous file to: billing-errors-2025.
Deleted original file from bucket.
```

---

## 📌 Validation Rules

Each row is checked for:

* ✅ **Valid product line**: Must be one of `['Bakery', 'Meat', 'Dairy']`
* 💵 **Valid currency**: `USD`, `CAD`, or `MXN`
* 💰 **Non-negative bill amount**
* 📅 **Date format**: Must be `YYYY-MM-DD`

Files that fail validation are copied to the error bucket and deleted from the source.

---

## ⚡ Deploy to AWS

1. Upload the Lambda code using the AWS Toolkit
2. In the Lambda console, attach the `AmazonS3FullAccess` policy to your execution role *(for testing only)*
3. Add an S3 trigger:

   * Source: `billing-2025`
   * Event type: `PUT`

Now every `.csv` uploaded to `billing-2025` will trigger the Lambda function automatically.

---

## 🛠 Example Use Cases

* Financial document validation pipelines
* Real-time ingestion validation for SaaS billing tools
* Preprocessing raw data before analytics workflows

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Let's Connect

Have ideas to extend this? Need help with Lambda, S3, or Python on AWS?

Feel free to connect on [LinkedIn](https://www.linkedin.com/in/nmihaly) or open an issue!
