#
# This code generates insight 5 
# It is to compare the number of strokes vs correctness of the guess 
#
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight5.py
#

#
# History of the file
#*********************
#
# Nov 21 2019 - Creation - riat
# Nov 29 2019 - Code formatting and edited connection to MongDB - riat 
# Dec 03 2019 - code revisit - asundarr
# 

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight5').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
 
#   Read the required fields and get the size of the drawing field which corresponds to the number of strokes
    df_strokes_count = df.select(df['word'],df['recognized'],df['drawing'],functions.size(df['drawing']).alias("NumOfStrokes"))
    df_strokes_count.cache()

#   Find the number of guesses which were correct for a particular number of strokes
    df_true_filter = df_strokes_count.where(df['recognized']=='true')
    df_true_occ_count = df_true_filter.groupby('NumOfStrokes').agg(functions.count('recognized')).select(df_true_filter['NumOfStrokes'],functions.col('count(recognized)').alias('true_count'))

#   Find the number of guesses in total for a particular number of strokes
    df_all_count = df_strokes_count.groupby('NumOfStrokes').agg(functions.count('recognized')).select(df_strokes_count['NumOfStrokes'],functions.col('count(recognized)').alias('all_count'))

#   Join the dataframes to bring everything together
    df_join = df_true_occ_count.join(df_all_count, df_true_occ_count['NumOfStrokes']==df_all_count['NumOfStrokes']).select(df_true_occ_count['*'],df_all_count['all_count'])

#   Find the accuracy by calculating the percentage of the true guesses
    df_accuracy = df_join.select(df_join['*'],((df_join['true_count']/df_join['all_count'])*100).alias('accuracy'))
    df_final=df_accuracy.sort(df_accuracy['NumOfStrokes'])
    
#   Load the results to a mongodb collection
    df_final.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight5").mode("overwrite").save()
   
if __name__ == '__main__':
   main()
