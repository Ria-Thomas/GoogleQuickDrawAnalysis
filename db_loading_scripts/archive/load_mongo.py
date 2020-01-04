#
# This file is the first of the files written to populate the data into mongodb
# Makes use of the spark way to load the data into mongodb
# 
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 load_mongo.py quickdraw_test
#

#
# History of the file
#*********************
#
# Nov 2 2019 - creation - riat
# Nov 17 2019 - adding changes to load the mongodb in VM - asundarr
#

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import com.mongodb.spark._
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.master('local').config('spark.mongodb.output.uri','mongodb://localhost:27017/BigDataTrio732.QuickDrawData').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')
# add more functions as necessary
def main(inputs):
   file_schema = types.StructType([
   types.StructField('word', types.StringType()),
   types.StructField('countrycode', types.StringType()),
   types.StructField('timestamp', types.StringType()),
   types.StructField('recognized', types.BooleanType()),
   types.StructField('key_id', types.StringType()),
   types.StructField('drawing', types.StringType())
   ])
   df = spark.read.json(inputs, schema=file_schema)
   #df.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://localhost:27017/BigDataTrio732.QuickDrawData").mode("append").save()
   df.write.format("com.mongodb.spark.sql.DefaultSource").mode("overwrite").option("database","BigDataTrio").option("collection","QuickDrawData").save()
#localhost:27017
if __name__ == '__main__':
   inputs = sys.argv[1]
   main(inputs)
