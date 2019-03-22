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

storage_account_name = "databricksiw"
storage_account_access_key = "XTwGvPpENbQyYHtFpFQRuFdqZshKc8rcYmUnEtjaUVzpUBDw+2odX0lMXx8cTj8MzbynLwRaqGR4DUwvKFe2Mw=="
contenedor = "databricks"
spark.conf.set(
  "fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
  storage_account_access_key)

# COMMAND ----------

# MAGIC %md
# MAGIC ####2. Cargue los archivos

# COMMAND ----------

file_location = "wasbs://"+contenedor+"@"+storage_account_name+".blob.core.windows.net/MuertesViolentas.csv"
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

df.createOrReplaceTempView("MuertesViolentas")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from MuertesViolentas
# MAGIC where manera_de_muerte <> 'Total'

# COMMAND ----------

# MAGIC %md
# MAGIC ####7. Listo, guardemos para uso posterior

# COMMAND ----------

df.write.format("parquet").saveAsTable("MuertesViolentas")