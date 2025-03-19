# LAMBDA SAVE FILE S3

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Lambda_Kaggle_Extraccion  README](./docs/Lambda_Kaggle_Extraccion.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Crawler_S3_to_Glue-DataCatalog](./docs/Crawler_S3_to_Glue-DataCatalog.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Configuración AWS Lambda)

#### 1. Creación de la Lambda

- En AWS buscar el servicio "Lambda", dar clic en "Crear una función" y realizar las siguientes parametrizaciones:
- Crear desde cero
- Nombre de la función: "Lambda_Save_File_S3"
- Tiempo de ejecución: Seleccionar "Python 3.13" o la versión más reciente.
- Arquitectura: x86_64
- Rol de ejecución: Seleccionar "Uso de un rol existente" y seleccionar "Nombre del rol". (Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Dar clic en "Crear una función"
- Revisar en "Lambda/Funciones" la visualización de "Lambda_Save_File_S3"


#### 2. Configuración de la Lambda

- En AWS ingresar a "Lambda/Funciones" y dar clic en "Lambda_Save_File_S3".

#### 2.1 Configuración Capas

- Dar clic en "Añadir una capa" y realizar los siguientes pasos: 
- Capa Pandas: Dar clic en "Especificar un ARN" y pegar el ARN de pandas 3.13 "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python313:1"


#### 2.2 Configuración Parametros

- Dar clic en "Configuración" y en "Editar" (Modificaciónd de los parametros iniciales)
- Modificar el "Tiempo de espera", por defecto es "3 seg", se sugiere aumentarlo de 3-5 minutos.
- Dar clic en "Guardar"

#### 4. Código de la Lambda

- Revisar el script [Lambda_Save_File_S3.py](ETL_Transacciones_Fraudulente_PowerBI/scripts/Lambda_Save_File_S3.py)


#### 5. Ejecución de la Lambda

- Dar clic en "Deploy", esperar al mensaje de confirmación.
- Dar clic en "Test", esperar el mensaje de confirmación.

#### 6. Validación del proceso

- En la pestaña "OUTPUT", debe aparecer el siguiente mensaje:

Response:
{
  "statusCode": 200,
  "body": "Archivos procesados y subidos exitosamente a S3:\n- Original: s3://report-fraud-transaction/datasets/CreditCardData.csv\n- Transformado: s3://report-fraud-transaction/datasets/dataClean_CreditCard_Transform.csv"
}

- Validar en el BUCKET de S3, la existencia del archivo csv "CreditCardData.csv" en el PATH: "report-fraud-transaction/datasets/dataClean_CreditCard_Transform.csv"




## Configuraciones Adicionales

#### 1. Creación del Rol

##### 1.1 Ingresar al servicio de AWS "IAM"
##### 1.2 Seleccionar "Roles" y dar clic en "Crear rol"
##### 1.3 Realizar la siguiente parametrización.

- Tipo de entidad de confianza: "Servicio de AWS"
- Caso de uso: "Lambda" y dar clic en "Siguiente"
- Politica de permisos: Seleccionar "AmazonS3FullAccess" y dar clic en "Siguiente"
- Asignar nombre de "Lambda_S3"
- Dar clic en "Crear rol"
