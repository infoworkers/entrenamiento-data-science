# Databricks notebook source
# MAGIC %md
# MAGIC ###Importe la libreria de MLFlow al cluster
# MAGIC http://blog.iwco.co/2019/03/28/como-agregar-librerias-a-databricks/

# COMMAND ----------

import mlflow

# COMMAND ----------

# MAGIC %md
# MAGIC Demosle un nombre al experimiento

# COMMAND ----------

mlflow.set_experiment("/Shared/MiExperimiento")

# COMMAND ----------

# MAGIC %md
# MAGIC Iniciemos una ejecucion de MLFlow

# COMMAND ----------

with mlflow.start_run() as run:
  mlflow.log_param("Parametro", 5)
  mlflow.log_metric("dato", 1)
  mlflow.log_metric("dato", 2)
  mlflow.log_metric("dato", 3)
with open("salida.txt", "w") as f:
    f.write("Hola mundo")
mlflow.log_artifact("salida.txt")