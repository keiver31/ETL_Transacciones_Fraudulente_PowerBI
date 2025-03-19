import os
import boto3
import pandas as pd
import io

# Configuración de AWS S3
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "report-fraud-transaction")
S3_FILE_KEY = os.getenv("S3_FILE_KEY", "datasets/CreditCardData.csv")
TMP_FILE_PATH = "/tmp/CreditCardData.csv"
CLEAN_FILE_NAME = os.getenv("CLEAN_FILE_NAME", "dataClean_CreditCard_Transform.csv")

# Inicializar cliente S3
s3_client = boto3.client("s3")

def download_from_s3(bucket_name, s3_key, local_path):
    """ Descarga un archivo de S3 y lo guarda en /tmp/ """
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"Archivo descargado desde S3: {s3_key}")
        return local_path
    except Exception as e:
        print(f"Error descargando archivo de S3: {str(e)}")
        return None

def upload_to_s3(file_path, bucket_name, s3_key):
    """ Sube un archivo local a S3 """
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Archivo subido a S3: s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error subiendo archivo a S3: {str(e)}")

def transform_dataset(file_path):
    """ Realiza transformaciones en el dataset y lo guarda en /tmp/ """
    df = pd.read_csv(file_path, dtype=str, delimiter=",", skipinitialspace=True)

    # Renombrar columnas reemplazando espacios por guiones bajos
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # Limpiar 'Transaction_ID' eliminando caracteres no numéricos
    df["Transaction_ID"] = df["Transaction_ID"].str.replace(r"[# ]", "", regex=True).astype("int64")

    # Limpiar y convertir 'Amount' eliminando símbolos y comas
    df["Amount"] = df["Amount"].replace(r"[£,]", "", regex=True).astype(float)

    # Convertir la fecha a datetime
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")

    # Convertir columnas a sus tipos finales
    column_types = {
        "Transaction_ID": "int64",
        "Day_of_Week": "string",
        "Time": "int64",
        "Type_of_Card": "string",
        "Entry_Mode": "string",
        "Type_of_Transaction": "string",
        "Merchant_Group": "string",
        "Country_of_Transaction": "string",
        "Shipping_Address": "string",
        "Country_of_Residence": "string",
        "Gender": "string",
        "Age": "float64",
        "Bank": "string",
        "Fraud": "int64"
    }
    df = df.astype(column_types)

    # Guardar archivo transformado en /tmp/
    transformed_file_path = f"/tmp/{CLEAN_FILE_NAME}"
    df.to_csv(transformed_file_path, index=False)
    
    return transformed_file_path

def lambda_handler(event, context):
    """ Función principal de la Lambda """
    # Descargar archivo desde S3
    dataset_path = download_from_s3(S3_BUCKET_NAME, S3_FILE_KEY, TMP_FILE_PATH)
    
    if dataset_path:
        # Transformar el dataset
        transformed_path = transform_dataset(dataset_path)
        
        # Subir el archivo transformado a S3
        upload_to_s3(transformed_path, S3_BUCKET_NAME, f"datasets/{CLEAN_FILE_NAME}")

        return {
            'statusCode': 200,
            'body': f"Archivos procesados y subidos exitosamente a S3:\n"
                    f"- Original: s3://{S3_BUCKET_NAME}/{S3_FILE_KEY}\n"
                    f"- Transformado: s3://{S3_BUCKET_NAME}/datasets/{CLEAN_FILE_NAME}"
        }
    
    return {
        'statusCode': 500,
        'body': "Error: No se encontró el archivo en S3"
    }