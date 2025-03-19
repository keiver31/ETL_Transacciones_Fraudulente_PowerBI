# CREACIÓN DE RDS y Base de Datos

Importante: 
- Antes de iniciar la configuración descrita en esta sección, se deben realizar los pasos de [Crawler_S3_to_Glue-DataCatalog README](./docs/Crawler_S3_to_Glue-DataCatalog.md)
- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Job DataCatalog_to_RDS README](./docs/DataCatalog_to_RDS.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Creación de la Base de Datos)

#### 1. Creación de la Base de Datos

- En AWS buscar el servicio "Aurora and RDS", dar clic en "Bases de datos" y "Crear base de datos", realizar las siguientes parametrizaciones:
- Elegir un método de creación de base de datos: Creación estándar
- Tipo de motor: MySQL
- Versión del motor: MySQL 8.0.40
- Plantillas: Producción
- Disponibilidad y durabilidad/Opciones de implementación: Implementación de una instancia de base de datos de zona de disponibilidad única (1 instancia)
- Identificador de instancias de bases de datos: database-2
- Administración de credenciales: Autoadministrado (definir "Nombre de usuario maestro" y "Contraseña maestra")
- Clase de instancia de base de datos:Clases ampliables (incluye clases t), seleccionar "db.t3.micro"
- Tipo de almacenamiento: SSD de uso general(gp2)
- Almacenamiento asignado: 20
- Configuración de almacenamiento adicional/Umbral de almacenamiento máximo: 25
- Recurso de computación:No se conecte a un recurso informático EC2
- Acceso público: NO
- Grupo de seguridad de VPC (firewall): Elegir existente
- Grupos de seguridad de VPC existentes: Seleccionar "s3-glue-rds" o crear el grupo de seguridad(Revisar sección "Configuraciones Adicionales/Creación del Grupo de Seguridad")
- Zona de disponibilidad: De preferencia, manejar todo en la misma zona, es decir, elegir "us-east-1a" para este caso
- Autenticación de bases de datos: Autenticación con contraseña
- Dar clic en "Crear base de datos"
- Revisar en "Aurora and RDS/Bases de datos" la visualización de "database-2" y que el campo "Estado" este en "Disponible".


#### 2. Validación de la conexión desde el local

- Descargar "sqlelectron" y configurarlo, despues de esto dar clic en abrir.
- Dar clic en "Add" y configurar de la siguiente manera:
- Name: rds_to_mysql(o el nombre que considere)
- Server Address/Host: Valor correspondiente a "Punto de enlace" de la base de datos.
- Server Address/Port: Puerto designado en la base de datos.
- User: Correspondientes a los valores de "Administración de credenciales"
- Dar clic en "Test", si se obtiene un resultado exitoso, dar clic en "Save"

#### 3. Configuración de la base de datos desde el local

- En el "rds_to_mysql" de "sqlelectron" dar clic en "Connect".
- En el script de "sqlelectron", llevar a cabo la creación de la base de datos, la tabla y los campos de las columnas, con los siguientes comandos:
- Creación de la base de datos:
CREATE DATABASE db_report_fraud_bank_v2

- Creación de la tabla:
USE db_report_fraud_bank_v2;

CREATE TABLE dataclean_creditcard_transform_csv (
    transaction_ID BIGINT,
    date VARCHAR(20),
    day_of_week VARCHAR(20),
    time BIGINT,
    type_of_Card VARCHAR(50),
    entry_mode VARCHAR(50),
    amount FLOAT,
    type_of_transaction VARCHAR(100),
    merchant_group VARCHAR(100),
    country_of_transaction VARCHAR(50),
    shipping_address VARCHAR(255),
    country_of_residence VARCHAR(50),
    gender VARCHAR(10),
    age FLOAT,
    bank VARCHAR(100),
    fraud TINYINT
);


#### 4. Validación del proceso desde el local

- Despues de ejecutar el "job" en [Job DataCatalog_to_RDS README](./docs/DataCatalog_to_RDS.md), se valida si los registros se cargaron en AWS RDS, entonces con la conexión de "sqlelectron" a "AWS RDS", se ejecuta el siguiente comando:

USE db_report_fraud_bank_v2;
SELECT * FROM dataclean_creditcard_transform_csv LIMIT 10;

- Si se observan los registros en "sqlelectron", esto quiero decir que la data se cargo de forma correcta a AWS RDS desde Glue y que la conexión entre AWS RDS y "sqlelectron", esta activa y funciona.

### Configuraciones Adicionales

#### 1. Creación del Grupo de Seguridad

##### 1.1 Ingresar al servicio de AWS "EC2"
##### 1.2 Seleccionar "Security Groups" y dar clic en "Crear grupo de seguridad"
##### 1.3 Realizar la siguiente parametrización.

- Nombre del grupo de seguridad: s3-glue-rds
- ID de la regla del grupo de seguridad: Seleccionar
- Tipo: MYSQL/Aurora
- Protocolo: TCP
- Intervalo de puertos: Elegir el correspondiente
- Origen: Personalizada
- IP: Parametrizar la correspondiente
- Dar clic en "Guardar reglas"


