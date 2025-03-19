# INTEGRACIÓN ENTRE GLUE DATACATOLOG Y RDS

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Creación RDS_MySQL README](./docs/RDS_MySQL.md)


Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Integración entre GLUE y RDS)

#### 1. Parametrización de datos 

- En AWS buscar el servicio "AWS Glue", dar clic en "ETL jobs" y "Script editor", realizar las siguientes parametrizaciones:
- En la ventana "Script" seleccionar "Spark" y dar clic en "Create script"
- En la sección "Job details", marcar los siguientes campos:
- Asignar el nombre de "etl_s3_to_rds_v2.0".
- IAM Role: Seleccionar el rol o realizar la creación del rol(Revisar sección "Configuraciones Adicionales/Creación del Rol")
- Requested number of workers: Ingresar 10(se pueden seleccionar más o menos de acuerdo a la necesidad)

#### 1.1. Código del Job

- En la sección "Script", incluir el código.
- Revisar el código en [DataCatalog_to_RDS.py](ETL_Transacciones_Fraudulente_PowerBI/scripts/DataCatalog_to_RDS.py)
- En los campos "USUARIO_ROOT", "CLAVE_ROOT" y "jdbc:mysql://<Punto de enlace>:<Puerto>/db_report_fraud_bank_v2", asignar los valores respectivos.
- Dar clic en "Save" y luego en "Run".
- Buscar la ruta "AWS Glue/ETL jobs" y dar clic sobre "etl_s3_to_rds_v2.0", este debe estar en ejecución o debe haber terminado de ejecutar.
-En la sección "Runs", en el campo "Run status", aparece el estado, si el proceso se realizo de manera exitosa, este debe de marcar "Succeded"


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



