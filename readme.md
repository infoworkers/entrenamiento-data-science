# Taller de Azure databricks

Elementos necesarios para el taller
===================================
1. Una instancia de Azure Databricks  
2. Una instancia de SQL Server
3. Una cuenta de almacenamiento en Azure
4. Instalar Power BI Desktop. (https://powerbi.microsoft.com/es-es/desktop/?WT.mc_id=Blog_Desktop_Update)
5. Instalar SSMS - Sql Server Management Studio. (https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-2017)

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Finfoworkers%2Fentrenamiento-data-science%2Fmaster%2Farm%2Fcrear-databricks.json" target="_blank">Clic para desplegar a Azure</a>

Siga los pasos para desplegar todo en Azure y espere a que esto termine, el proceso no tardará mas de unos minutos.

#aqui va la imagen

Vaya a su suscripción de Azure y abra el Shell de Azure (Otra imagen)

Para habilitar el Azure DWH, en el shell copie y pegue el siguiente codigo
```
$GrupoDeRecursos = "<Grupo de recursos>"
$Servidor = "<Nombre del servidor>"
$NombreBD = "BDDataBricks"
New-AzSqlDatabase -ResourceGroupName $GrupoDeRecursos -ServerName $Servidor -DatabaseName $NombreBD -Edition "DataWarehouse" -RequestedServiceObjectiveName "DW2000" -CollationName "SQL_Latin1_General_CP1_CI_AS"
```
Para habilitar el Datafactory
```
$dataFactory = "<Nombre del Data factory>"
$localizacion = "East US 2"
$df = Set-AzDataFactoryV2 -ResourceGroupName $GrupoDeRecursos -Location $localizacion -Name $dataFactory
```
Ahora vamos a vincular nuestro almacenamiento
```
$json = "{
    ""name"": ""AzureStorageLinkedService"",
    ""properties"": {
        ""type"": ""AzureStorage"",
        ""typeProperties"": {
            ""connectionString"": {
                ""value"": ""DefaultEndpointsProtocol=https;AccountName=<CUENTA>;AccountKey=<LLAVE>;EndpointSuffix=core.windows.net"",
                ""type"": ""SecureString""
            }
        }
    }
}"
$cd = Get-CloudDrive
$salida ="$($cd.MountPoint)/salida.json"
$json | out-file $salida
$ls = Set-AzDataFactoryV2LinkedService -DataFactoryName $df.DataFactoryName -ResourceGroupName $GrupoDeRecursos -Name "AzureStorageLinkedService" -DefinitionFile $salida
```
Ahora vincularemos nuestro SQL DWH
```
$jsonSQL = "{
	""name"": ""AzureSqlLinkedService"",
	""properties"": {
		""type"": ""AzureSqlDatabase"",
		""typeProperties"": {
			""connectionString"": ""Server=tcp:<server>.database.windows.net,1433;Database=<databasename>;User ID=<user>@<server>;Password=<password>;Trusted_Connection=False;Encrypt=True;Connection Timeout=30""
		}
	}
 }"

 $jsonSQL | out-file $salidaSQL
 $lsSQL = Set-AzDataFactoryV2LinkedService -DataFactoryName $df.DataFactoryName -ResourceGroupName $GrupoDeRecursos -Name "AzureSqlLinkedService" -DefinitionFile $salidaSQL
 ```
## Crear el pipeline en Datafactory

Realizar los pasos de la primera sesión para cargar la data de los siguientes links:

https://www.datos.gov.co/Econom-a-y-Finanzas/DNP-SeguimientoProyecto/pskh-spdv

https://www.datos.gov.co/Econom-a-y-Finanzas/DNP-proyectos_datos_basicos/cf9k-55fw

1. Azure Blob Storage
2. Azure Data Warehouse (Crear la tabla a través del SSMS - Proyectos básicos)
2.1 Crear esquema
```
CREATE SCHEMA <Nombre_Esquema>
```
2.2 Crear tabla
```
CREATE TABLE <Nombre_Esquema>.<Nombre_tabla>(
Bpin nvarchar(3000),
NombreProyecto nvarchar(3000),
ObjetivoGeneral nvarchar(3000),
Problematica nvarchar(3000),
EstadoProyecto nvarchar(3000),
Horizonte nvarchar(3000),
FechaAprobacion nvarchar(3000),
Sector nvarchar(3000),
EntidadResponsable nvarchar(3000),
EntidadEjecutora nvarchar(3000),
Programa nvarchar(3000),
ConpesAsociado nvarchar(3000),
TipoPlanDesarrollo nvarchar(3000),
PeriodPlanDesarrollo nvarchar(3000),
NombrePlanDesarrollo nvarchar(3000)
)
```

# Consumir data desde Databricks

## Conexión al Blob storage desde Databricks

1. Crear conexión al storage.

```
storage_account_name = "<cuenta de almacenamiento>"
storage_account_access_key = "<Llave>"
contenedor = "<Contenedor>"
spark.conf.set(
  "fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
  storage_account_access_key)
```
2. Cargue los archivos.

```
file_location = "wasbs://"+contenedor+"@"+storage_account_name+".blob.core.windows.net/<Nombre_archivo>"
file_type = "csv"
```

3. Creemos un dataframe.
```
df = spark.read.format(file_type).option("inferSchema", "true").option("header", "true").load(file_location)
```

4. Conusltemos los datos cargados desde el databricks.
```
df
import pandas as pd
pd_df = df.toPandas()
pd_df
```
5. Consultemos la tabla con usando SQL.
```
df.createOrReplaceTempView("<Nombre de la tabla>")

%sql
SELECT * FROM <Nombre de la tabla>
```
Probar otras consultas

6. Guardar dentro de Databricks.
```
df.write.format("parquet").saveAsTable("<Nombre_Tabla>")
```

## Conectar desde Power BI (Visualización)
### Databricks

1. Habilitar en databricks la creación de personal access token.
2. Crear access token.
3. Identificar la cadena de conexión del Databricks con Power BI.
4. Traer data a Power BI.

### DWH
1. Establecer conexión entre DWH y Power BI.
2. Traer data a Power BI

Realizar visualizaciones en Power BI



