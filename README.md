## 📰 News Data Pipeline with Airflow, AWS & Snowflake

### Overview
This project automates fetching, storing, verifying, and loading news data using Apache Airflow, AWS, and Snowflake. It ensures daily data integrity and timely notifications.

### 🏗 Tech Stack
- **Apache Airflow**: Orchestrates the end-to-end workflow.
- **AWS Lambda**: Fetches real-time news data.
- **Amazon S3**: Stores fetched news data.
- **Snowflake**: Stores and processes structured data.
- **Python & SQL**: Used for automation and querying.

### 🔄 Workflow
1. AWS Lambda fetches news data and stores it in an S3 bucket.
2. Airflow DAG verifies the file in S3.
3. If the file exists:
   - A Snowflake table is created (if not exists).
   - The data is loaded into Snowflake.
   - A success email notification is sent.
4. If the file is missing, the DAG fails and triggers an alert.


