# workspace/spark_utils.py

from pyspark.sql import SparkSession # type: ignore

def get_spark():
    """Create and return a SparkSession."""
    return SparkSession.builder.appName("Pipezone").getOrCreate()