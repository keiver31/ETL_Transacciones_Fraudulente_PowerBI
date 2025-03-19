
# LAMBDA KAGGLE EXTRACCION

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Creación Bucket S3 README](./docs/Bucket_S3.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Lambda_Save_File_S3 README](./docs/Lambda_Save_File_S3.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Configuración AWS Lambda)

#### 1. Creación de la Lambda

- En AWS buscar el servicio "Lambda", dar clic en "Crear una función" y realizar las siguientes parametrizaciones:
- Crear desde cero
- Nombre de la función: "Lambda_Kaggle_Extraccion"
- Tiempo de ejecución: Seleccionar "Python 3.13" o la versión más reciente.
- Arquitectura: x86_64
- Rol de ejecución: Seleccionar "Uso de un rol existente" y seleccionar "Nombre del rol". (Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Dar clic en "Crear una función"
- Revisar en "Lambda/Funciones" la visualización de "Lambda_Kaggle_Extraccion"


#### 2. Creación de la capa de Kaggle

En el Local del equipo, abrir el cmd y ejecutar los siguientes comandos para Windows:

- Remove-Item -Recurse -Force python
- New-Item -ItemType Directory -Path python\lib\python3.7\site-packages -Force
- docker run -v "$(Get-Location):/var/task" "public.ecr.aws/sam/build-python3.13" /bin/sh -c "pip install kaggle -t python/lib/python3.13/site-packages/; exit"
- Compress-Archive -Path python -DestinationPath kaggle.zip -Force

En el Local se debe generar un archivo llamado "kaggle.zip"

Nota: Validar que se este ejecutando Docker, al momento de correr los comandos anteriores.

#### 2.1 Cargue de Capa de Kaggle a AWS

- En AWS ingresar a la opción "Lambda"
- Seleccionar "Capas" y dar clic en "Crear capa"
- Asignar el nombre de "Kaggle_Lambda_Extraccion_Comprimido", dar clic en "Cargar un archivo .zip" y seleccionar el archivo "kaggle.zip"-
- Dar clic en "Crear"
- Revisar en "Lambda/Capas" que se visualice: "Kaggle_Lambda_Extraccion_Comprimido"

Nota: Ingresar a "Kaggle_Lambda_Extraccion_Comprimido" y copiar el "ARN de la versión"

#### 3. Configuración de la Lambda

- En AWS ingresar a "Lambda/Funciones" y dar clic en "Lambda_Kaggle_Extraccion".

#### 3.1 Configuración Capas

- Dar clic en "Añadir una capa"(esto se debe realizar dos veces) y realizar los siguientes pasos: 
- Capa Kaggle: Dar clic en "Especificar un ARN" y pegar el "ARN de la versión" de "Kaggle_Lambda_Extraccion_Comprimido" y dar clic en "Agregar"
- Capa Pandas: Dar clic en "Especificar un ARN" y pegar el ARN de pandas 3.13 "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python313:1"


#### 3.2 Configuración Parametros

- Dar clic en "Configuración" y en "Editar" (Modificación de los parametros iniciales)
- Modificar el "Tiempo de espera", por defecto es "3 seg", se sugiere aumentarlo de 3-5 minutos.
- Dar clic en "Guardar"

#### 4. Código de la Lambda

- Revisar el script [Lambda_Kaggle_Extraccion.py](./scripts/Lambda_Kaggle_Extraccion.py)
- En los campos "KAGGLE_USERNAME" y "KAGGLE_KEY", asignar las credenciales de ingreso.

#### 5. Ejecución de la Lambda

-Dar clic en "Deploy", esperar al mensaje de confirmación.
-Dar clic en "Test", esperar el mensaje de confirmación.

#### 6. Validación del proceso

- En la pestaña "OUTPUT", debe aparecer el siguiente mensaje:

Response:
{
  "statusCode": 200,
  "body": "Archivo subido exitosamente a S3: s3://report-fraud-transaction/datasets/CreditCardData.csv"
}

- Validar en el BUCKET de S3, la existencia del archivo csv "CreditCardData.csv" en el PATH: "report-fraud-transaction/datasets/CreditCardData.csv"




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



