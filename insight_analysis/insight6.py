#
# This file generates insight number 6 
# The insight of providing the details of which country recognised a given image correctly maximum number of times
# 
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight6.py
#

#
# History of the file
#*********************
#
# Nov 28 2019 - creation - asundarr
# Nov 29 2019 - Code formatting and edited the mongodb connection - riat
# Dec 03 2019 - code revisit - asundarr
# 

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import com.mongodb
from pyspark.sql import SparkSession, functions, types
from pyspark.sql.functions import broadcast
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight6').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

   df_read = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

#  Filter the correctly guessesd records and find the maximum count for each word
   df1 = df_read.filter(df_read["recognized"] == "true")
   df2 = df1.groupby('countrycode', 'word', 'recognized').count().orderBy('word').cache()
   df3 = df2.groupby('word').agg(functions.max('count'))

#  Join the dataframes to get the required fields
   join_cond = [df3['word'] == df2['word'], df3['max(count)'] == df2['count']]
   df_join = df2.join(df3, join_cond).select(df2['word'], df2['countrycode'], df3['max(count)'])

#  Load the results to a mongodb collection  
   df_join.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight6").mode("overwrite").save()
       
if __name__ == '__main__':
   main()	
