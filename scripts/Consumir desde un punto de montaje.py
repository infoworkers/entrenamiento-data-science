# Databricks notebook source
import pandas as pd

# COMMAND ----------

dbutils.fs.ls("/mnt/misdatos")
archivo = "/mnt/misdatos/MuertesViolentas.csv"
tipo = "csv"
df = spark.read.format(tipo).option("inferSchema", "true").option("header", "true").load(archivo)

# COMMAND ----------

df.toPandas()