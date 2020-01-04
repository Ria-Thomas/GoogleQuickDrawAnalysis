#
# This file generates the insight number 3 
# The insight of providing the details of what time of the day people of which country are busy using this application.
# 
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight3.py
#

#
# History of the file
#*********************
#
# Nov 21 2019 - creation - asundarr
# Nov 29 2019 - Code formatting and edited connection to MongDB - riat 
# Dec 03 2019 - code revisit - asundarr
# 

import sys
import datetime
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import com.mongodb
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight3').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

# UDF to split the timestamp to get the time part and assign part of the day to each hour
@functions.udf(returnType=types.StringType())
def get_part_of_day(date):
   date0 = date.split(" ")
   day = date0[1]
   day_split = day.split(":")
   hour = int(day_split[0])
   return (
        "morning" if 5 <= hour <= 11
        else
        "afternoon" if 12 <= hour <= 17
        else
        "evening" if 18 <= hour <= 22
        else
        "night"
   )
   

def main():
   
   df_read = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

#  Get the required fields and call the udf    
   df_test = df_read.select('timestamp', 'countrycode').cache()
   partofday = df_test.withColumn("timeofday", get_part_of_day(df_test['timestamp']))

#  Find the count of active instances in each part of the day   
   partofday_count = partofday.groupby('countrycode', 'timeofday').count().orderBy('countrycode')
   
#  Load the results to a mongodb collection
   partofday_count.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight3").mode("overwrite").save() 

if __name__ == '__main__':
   main()	
