# Databricks notebook source
# MAGIC %md
# MAGIC ##Como crear un punto de montaje en Blob Storage

# COMMAND ----------

dbutils.fs.mount(
  source = "wasbs://databricks@databricksiw.blob.core.windows.net/",
  mount_point = "/mnt/misdatos",
  extra_configs = {"fs.azure.account.key.databricksiw.blob.core.windows.net":"BYFafvUq0A10FIUWBk5nLTyV8rt4tLBDX3aO5dpyCr3eyJ+gJ1p2v0tQgpaCQ5wFA5U8v7pzh9bvK/TDaWeIxg=="})

# COMMAND ----------

dbutils.fs.ls("/mnt/misdatos")