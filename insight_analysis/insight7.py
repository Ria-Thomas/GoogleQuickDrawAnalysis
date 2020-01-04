#
# This code generates insight 7 
# To find the avg number of strokes drawn by users of each country for a particular object
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight7.py
#

#
# History of the file
#*********************
#
# Dec 3 2019 - Creation - vvenugop
# Dec 3 2019 - Code formatting and edited connection to MongDB - vvenugop 

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight7').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
 
#   Read the required fields such as word, countrycode and get the size of the drawing field (the number of strokes) that correspons to each word
    df_strokes_count = df.select(df['word'],df['countrycode'],df['recognized'],df['drawing'],functions.size(df['drawing']).alias("NumOfStrokes"))
    df_strokes_count.cache()
 	
#   Find the number of guesses which were correct for a particular number of strokes
    df_true_filter = df_strokes_count.where(df['recognized']=='true')
    df_true_filter.createOrReplaceTempView('table1')
    final= spark.sql('SELECT word,countrycode,round(avg(NumOfStrokes)) as AvgNumOfStrokes from table1 group by word,countrycode')
        
#   Load the results to a mongodb collection
    final.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight7").mode("overwrite").save()
   
if __name__ == '__main__':
   main()
