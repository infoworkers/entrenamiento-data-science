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
  mlflow.log_param("param1", 5)
  mlflow.log_metric("foo", 1)
  mlflow.log_metric("foo", 2)
  mlflow.log_metric("foo", 3)
with open("salida.txt", "w") as f:
    f.write("Hola mundo")
mlflow.log_artifact("salida.txt")