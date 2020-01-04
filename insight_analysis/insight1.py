#
# This file generates the insight number 1 
# The insight of providing the details of which images are the most popular ones in each country.
# 
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight1.py
#

#
# History of the file
#*********************
#
# Nov 20 2019 - creation - asundarr
# Nov 28 2019 - code cleanup and changes to run on gateway - asundarr
# Dec 03 2019 - code revisit - asundarr
# 

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import com.mongodb
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight1').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

#  Read from the main collection 
   df_read = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

#  Group by countrycode and word to find the count of each word and find the word which has the maximum count
   df_test = df_read.groupby('countrycode', 'word').count()
   df_test_max =  df_test.select(df_test['countrycode'], df_test['word'], df_test['count'].alias('counts')).orderBy('countrycode').cache()
   df_test_max_country = df_test_max.groupby('countrycode').agg(functions.max('counts')).orderBy('countrycode')
   
#  Join the dataframe with the maximum count with the original dataframe to get the the required fields.
   join_cond = [df_test_max['countrycode'] == df_test_max_country['countrycode'], df_test_max['counts'] == df_test_max_country['max(counts)']]
   df_join = df_test_max_country.join(df_test_max, join_cond).select(df_test_max['countrycode'], 'word', 'counts').orderBy('countrycode')

#  Store the results in a different mongodb collection
   df_join.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight1").mode("overwrite").save()

if __name__ == '__main__':
   main()	
