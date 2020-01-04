#
# This file is used for Using Gaussian naive bayes Classification
# The insight of providing the details of Using Gaussian naive bayes Classification on the given dataset interms pediction for the dataset.
# 
# Here is the way to run the file: ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 load_ml_data.py  
#

#
# History of the file
#*********************
#
# Nov 23 2019 - Creation - riat
# Nov 29 2019 - Code formatting and edited the mongdb collection - riat


import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://useradmin:passwordbdt@nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://useradmin:passwordbdt@nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.MLData').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

#   Read only the drawings with 1 stroke
    df1=df.where(functions.size(df['drawing'])==1)

#   Find the number of elements in each drawing matrix (represents the number of pixels)
    df2 = df1.select(df1['recognized'],functions.flatten(df1['drawing']).alias("drawing1"))
    df3 = df2.select(df2['recognized'],functions.flatten(df2['drawing1']).alias("drawing2"))
    df4 = df3.select(df3['recognized'],df3['drawing2'], functions.size(df3['drawing2']).alias("NumOfElements"))

#   Find the maximum count for the elements
    df4.createOrReplaceTempView('df4')
    df5 = spark.sql("select NumOfElements,count(*) as cnt from df4 group by NumOfElements having count(*)>1 order by cnt DESC")
    df6 = df5.groupby().agg(functions.first(df5['NumOfElements']).alias('Max_num'))
    max_num=df6.select(df6['Max_num']).collect()

#   Filter only the elements with maximum count - Makes the dataset random and provides data for training.

    df7 = df4.where(df4['NumOfElements'] == int(max_num[0].Max_num))
    df8 = df7.select(df7['recognized'],df7['drawing2'])
    df9=df8.select([df8.recognized]+[df8.drawing2[i] for i in range(int(max_num[0].Max_num))])

#   Load the results into an intermediate collection to store dataset for applying classification models.
    df9.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri",'mongodb://useradmin:passwordbdt@nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.MLData").mode("append").save()

if __name__ == '__main__':
   main()
