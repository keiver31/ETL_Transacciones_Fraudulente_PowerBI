# CRAWLER DE S3 A GLUE DATACATALOG

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Lambda_Save_File_S3 README](./Lambda_Save_File_S3.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Creación RDS_MySQL README](./RDS_MySQL.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Creación del Crawler)

#### 1. Creación del Crawler

- En AWS buscar el servicio "AWS Glue", dar clic en "Crawlers" y "Create crawler", realizar las siguientes parametrizaciones:
- Nombre: "crawler_report_fraud_v2.0"
- Data source configuration: "Not yet"
- Data sources: Dar clic en "Add data source", en "S3 path", recorrer los folders hasta llegar al archivo csv, en el path "report-fraud-transaction/datasets/dataClean_CreditCard_Transform.csv" y seleccionarlo, dar clic en "Add an S3 data source" y en "Next"
- IAM role/Existing IAM role: Seleccionar el rol o realizar la creación del rol(Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Output configuration/Target database: Seleccionar o crear la Base de Datos(Revisar sección "Configuraciones Adicionales/Creación de Base de Datos") y dar clic en "Next"
- Dar clic en "Create crawler"
- Revisar en "AWS Glue/Crawlers" la visualización de "crawler_report_fraud_v2.0"


#### 2. Ejecución del crawler

- En "AWS Glue/Crawlers" seleccionar "crawler_report_fraud_v2.0" y dar clic en "Run".
- Esperar la ejecución del crawler, al terminar de ejecutarse debe aparecer el campo "State" como "Ready" y el campo "Last run" como "Succeeded"

#### 3. Validación del proceso

- En "AWS Glue/Databases" validar la creación de la base de datos "db_report_fraud_bank_2.0".
- Ingresar a la base de datos y validar los parametros asociados como tablas y la fuente de los recursos, entre otros parametros. 
- En "AWS Glue/Databases/Tables" validar la creación de la tabla "dataclean_creditcard_transform_csv"


## Configuraciones Adicionales

#### 1. Creación del Rol

##### 1.1 Ingresar al servicio de AWS "IAM"
##### 1.2 Seleccionar "Roles" y dar clic en "Crear rol"
##### 1.3 Realizar la siguiente parametrización.

- Tipo de entidad de confianza: "Servicio de AWS"
- Caso de uso: "Glue" y dar clic en "Siguiente"
- Politica de permisos: Seleccionar la politica de permiso correspondiente y dar clic en "Siguiente"
- Asignar nombre de "gluetos3"
- Dar clic en "Crear rol"


#### 2. Creación de Base de Datos

##### 2.1 Ingresar al servicio de AWS "AWS Glue"
##### 2.2 Seleccionar "Databases" y dar clic en "Add database"
##### 2.3 Realizar la siguiente parametrización.

- Name: "db_report_fraud_bank_2.0"
- Dar clic en "Create database"