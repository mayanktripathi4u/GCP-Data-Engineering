# Building an Automated Data Pipeline for Sales Data in Google Cloud

## Step 1: Create Web Portal to upload the file.
From Kaggle.
    E-Commerce Data

Sample file for order.csv will contains below folumns.
Invoice, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

## Cloud Function which will get trigger once the file is landed to GCS Bucket.
1. Env: 2nd Gen
2. Name: sales_data_load
3. Region: us-central-1
4. Trigger: Cloud Storage
5. Finalize Method
6. Bucket --> select the bucket name
7. next
8. RunTime: Python

## Step 3: Create a BigQuery Dataset as "sales".
Table will be created by the GCP FUnction.

This function will create the table, if not exists.

## Step 4: 
In BQ, add few columns.
SELECT *, (Quantity * UnitPrice) AS Total_Cost FROM orders ORDER BY country;


