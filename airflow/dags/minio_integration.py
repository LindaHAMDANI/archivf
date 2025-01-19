# Import Python dependencies needed for the workflow
from urllib import request
from minio import Minio, S3Error
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pendulum
import os
import urllib.error

# Function to download the Parquet file
def download_parquet(**kwargs):
    url: str = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    filename: str = "yellow_tripdata"
    extension: str = ".parquet"
    month: str = pendulum.now().subtract(months=2).format('YYYY-MM')
    file_path = f"{filename}_{month}{extension}"
    
    try:
        # Download the file
        request.urlretrieve(url + file_path, file_path)
        print(f"Downloaded file: {file_path}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to download the parquet file: {str(e)}") from e

# Function to upload the file to Minio
def upload_file(**kwargs):
    client = Minio(
        "minio:9000",
        secure=False,
        access_key="minio-archi",
        secret_key="minio123"
    )
    bucket: str = 'rawnyc'
    month: str = pendulum.now().subtract(months=2).format('YYYY-MM')
    file_path = f"yellow_tripdata_{month}.parquet"

    # Ensure the bucket exists
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

    # Upload the file to the bucket
    client.fput_object(
        bucket_name=bucket,
        object_name=file_path,
        file_path=file_path
    )
    print(f"Uploaded {file_path} to bucket {bucket}.")

    # Remove the local file after successful upload
    os.remove(file_path)
    print(f"Removed local file: {file_path}")

# Define the DAG
with DAG(
    dag_id='grab_nyc_data_to_minio',  # Use a valid dag_id
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=['minio', 'read', 'write'],
) as dag:

    # Task 1: Download the Parquet file
    t1 = PythonOperator(
        task_id='download_parquet',
        provide_context=True,
        python_callable=download_parquet,
    )

    # Task 2: Upload the file to Minio
    t2 = PythonOperator(
        task_id='upload_file_task',
        provide_context=True,
        python_callable=upload_file,
    )

    # Define the task sequence
    t1 >> t2
