# Creación Bucket S3

Importante: 

- Despues de terminar de realizar la configuración descrita en esta sección, se deben realizar los pasos de [Lambda_Kaggle_Extraccion  README](./docs/Lambda_Kaggle_Extraccion.md)

Siguiendo el orden correcto, se pueden realizar los ajustes correspondientes para la configuración de esta lambda.

## Manual Paso a Paso(Creación del Bucket)

#### 1. Creación del Bucket

- En AWS buscar el servicio "S3", dar clic en "Crear bucket" y realizar las siguientes parametrizaciones:
- Tipo de bucket: Uso general
- Nombre del bucket: "report-fraud-transaction"
- Propiedad de objetos: ACL deshabilitadas (recomendado)
- Configuración de bloqueo de acceso público para este bucket: Seleccionar "Bloquear todo el acceso público"
- Control de versiones de buckets: Desactivar
- Tipo de cifrado: Cifrado del servidor con claves administradas de Amazon S3 (SSE-S3)
- Clave de bucket: Habilitar
- Dar clic en "Crear bucket"
- Revisar en "S3/Buckets" la visualización de "report-fraud-transaction"
