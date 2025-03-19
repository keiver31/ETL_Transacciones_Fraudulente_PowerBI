import json
import os
import boto3
os.environ["KAGGLE_CONFIG_DIR"] = "/tmp"
os.environ["KAGGLE_USERNAME"] = "KAGGLE_USERNAME"
os.environ["KAGGLE_KEY"] = "KAGGLE_KEY"

from kaggle.api.kaggle_api_extended import KaggleApi

s3_client = boto3.client('s3')

# Nombre del bucket de destino en S3
S3_BUCKET_NAME = "report-fraud-transaction"

def lambda_handler(event, context):
    api = KaggleApi()
    api.authenticate()
    dataset_path = "/tmp/"
    api.dataset_download_files('anurag629/credit-card-fraud-transaction-data', path=dataset_path,unzip=True)
    local_file_path = os.path.join(dataset_path, "CreditCardData.csv")
    if os.path.exists(local_file_path):
        s3_key = "datasets/CreditCardData.csv"
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, s3_key)
        return {
            'statusCode': 200,
            'body': f"Archivo subido exitosamente a S3: s3://{S3_BUCKET_NAME}/{s3_key}"
        }
    else:
        return {
            'statusCode': 500,
            'body': "Error: No se encontró el archivo en /tmp/"
        }