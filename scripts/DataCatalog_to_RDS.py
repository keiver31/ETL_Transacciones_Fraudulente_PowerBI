import sys
import boto3
import json
from pyspark.sql import SparkSession
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

# Inicializar sesión de Spark y contexto de Glue
spark = SparkSession.builder.getOrCreate()
glueContext = GlueContext(spark.sparkContext)
job = Job(glueContext)

# Obtener parámetros del job
args = getResolvedOptions(sys.argv, ['JOB_NAME']) if len(sys.argv) > 1 else {'JOB_NAME': 'default_job'}
job.init(args['JOB_NAME'], args)

# Leer datos desde Glue Data Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="db_report_fraud_bank_2.0",
    table_name="dataclean_creditcard_transform_csv"
)

# Verificar si hay datos disponibles
if datasource.count() == 0:
    raise Exception("No se encontraron datos en la tabla de Glue Data Catalog.")

# Convertir a DataFrame de Spark
df = datasource.toDF()

# Escribir en MySQL
df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://<Punto de enlace>:<Puerto>/db_report_fraud_bank_v2") \
    .option("dbtable", "dataclean_creditcard_transform_csv") \
    .option("user", "USUARIO_ROOT") \
    .option("password", "CLAVE_ROOT") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .mode("append") \
    .save()

# Finalizar el Job
job.commit()