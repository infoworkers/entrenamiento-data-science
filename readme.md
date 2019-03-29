# Taller de Azure databricks

Elementos necesarios para el taller
===================================
1. Una instancia de Azure Databricks  
2. Una instancia de SQL Server
3. Una cuenta de almacenamiento en Azure

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

#Consumir data desde Databricks

## Conexión al DWH y Blob storage desde Databricks
DWH:
Verificar conexion al DWH
```
Class.forName("com.databricks.spark.sqldw.DefaultSource")
```

