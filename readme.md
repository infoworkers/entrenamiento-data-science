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
New-AzSqlDatabase -ResourceGroupName $GrupoDeRecursos -ServerName $Servidor -DatabaseName $NombreBD -Edition "DataWarehouse" -RequestedServiceObjectiveName "DW2000" -CollationName "SQL_Latin1_General_CP1_CI_AS" -MaxSizeBytes 10995116277760
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
