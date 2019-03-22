# Databricks notebook source
# MAGIC %md
# MAGIC ##Como crear un punto de montaje en Blob Storage

# COMMAND ----------

dbutils.fs.mount(
  source = "wasbs://<contenedor>@<almacenamiento>.blob.core.windows.net/",
  mount_point = "/mnt/<sucarpeta>",
  extra_configs = {"fs.azure.account.key.<almacenamiento>.blob.core.windows.net":"<llave>"})

# COMMAND ----------

dbutils.fs.ls("/mnt/<sucarpeta>")