# type: ignore
# workspace/spark_utils.py

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext 

sqlContext = SQLContext(spark)

def get_spark():
    """Create and return a SparkSession."""
    return SparkSession.builder.appName("Pipezone").getOrCreate()