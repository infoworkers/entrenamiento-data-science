# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ##Taller basico de databricks (Information Workers)
# MAGIC Este taller está orientado a dar los primeros pasos en Databricks para el análisis de datos

# COMMAND ----------

# MAGIC %md
# MAGIC ####1. Cree una conexion al Storage
# MAGIC Utilizaremos el almacenamiento en un Blob Storage de Azure, de esta forma los datos van a residir fuera de nuestro cluster y no habrá problema en apagarlo.

# COMMAND ----------

storage_account_name = "<cuenta de almacenamiento>"
storage_account_access_key = "<Llave>"
contenedor = "<Contenedor>"
spark.conf.set(
  "fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
  storage_account_access_key)

# COMMAND ----------

# MAGIC %md
# MAGIC ####2. Cargue los archivos

# COMMAND ----------

#https://www.datos.gov.co/Estad-sticas-Nacionales/Cifras-preliminares-Muertes-violentas-seg-n-grupo-/68xb-xdyk
file_location = "wasbs://"+contenedor+"@"+storage_account_name+".blob.core.windows.net/datosejemplo.csv"
file_type = "csv"

# COMMAND ----------

# MAGIC %md
# MAGIC ####3. Creemos un dataframe

# COMMAND ----------

df = spark.read.format(file_type).option("inferSchema", "true").option("header", "true").load(file_location)

# COMMAND ----------

# MAGIC %md
# MAGIC ####4. Consultemos un dato

# COMMAND ----------

df

# COMMAND ----------

# MAGIC %md
# MAGIC ####5. Usemos Pandas

# COMMAND ----------

import pandas as pd

# COMMAND ----------

pd_df = df.toPandas()

# COMMAND ----------

pd_df

# COMMAND ----------

# MAGIC %md
# MAGIC ####6. Ahora usemos SQL

# COMMAND ----------

df.createOrReplaceTempView("Tabla")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from tabla
# MAGIC where grupo_de_edad <> 'Total'

# COMMAND ----------

# MAGIC %md
# MAGIC ####7. Listo, guardemos para uso posterior

# COMMAND ----------

df.write.format("parquet").saveAsTable("John")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from john

# COMMAND ----------

# MAGIC %md
# MAGIC ####Lab
# MAGIC Ahora hagan una tabla que traiga los datos de esta fuente
# MAGIC http://datosabiertos.bogota.gov.co/dataset/para-modificar/resource/30d65a8b-d0ed-4e95-977e-0d7cc2ea89ef