#
# This file generates the insight number 2_4 
# Find the images which the application guessed correctly the most or the least.
#
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight2_4.py
#

#
# History of the file
#*********************
#
# Nov 22 2019 - creation - vvenugop
# Dec 01 2019 - Code formatting and edited connection to MongDB - vvenugop 
# Dec 03 2019 - code revisit & adding more optimization - asundarr
# 

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight2_4').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

   df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
   df = df.select(df["word"], df["recognized"]).cache()
   df.createOrReplaceTempView('df')

   #Total no of time each word has been used
   top1=spark.sql("SELECT count(word)as total,word from df group by word")
   top1.createOrReplaceTempView('top1')

   #Total no of time each word has been recongnised by AI Bot- TRUE Cases
   top2=spark.sql("SELECT count(word)as trues,word from df where recognized='true' group by word")
   top2.createOrReplaceTempView('top2')

   #Total no of time each word has been  not recongnised by AI Bot- FALSE Cases
   top3=spark.sql("SELECT count(word)as false,word from df where recognized='false' group by word")
   top3.createOrReplaceTempView('top3')

   #TRUE and FALSE occurences for each word in percentage
   topfinal=spark.sql("SELECT t1.word,t2.trues, t3.false,(t2.trues/t1.total)*100 as truepercent,(t3.false/t1.total)*100 as falsepercent from top1 t1 inner join top2 t2 on t1.word=t2.word inner join top3 t3 on t1.word=t3.word")

   #Load the results to a mongodb collection
   topfinal.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight2_4").mode("overwrite").save()

if __name__ == '__main__':
   main()
