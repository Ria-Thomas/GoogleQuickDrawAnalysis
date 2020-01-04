# This file is for Insight 8
# The insight shows the precentage of clockwise and anticlockwise drawn circles for each country. This can represent the number of right-handed/left handed people and how the language they write shape the circles they draw
# 
# Here is the way to run the file: spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight8.py
#

#
# History of the file
#*********************
#
# Dec 1 2019 - Creation - riat


import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.QuickDrawData').config('spark.mongodb.output.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight8').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

#   Read the data only for the word,circle
    df1=df.where(df['word']=='circle')

#   Flatten the drawing array to fetch the x-coordinates
    df2 = df1.select(df1['countrycode'],functions.flatten(df1['drawing']).alias("drawing1"))
    df3 = df2.select(df2['countrycode'],functions.flatten(df2['drawing1']).alias("drawing2"))

#   Subtract x1 from x2 to find the direction of the curve. If x1>x2, the curve is anticlockwise and if x1<x2, the curve is clockwise    
    df4 = df3.select(df3['countrycode'],(df3['drawing2'][0]-df3['drawing2'][1]).alias('diff')).cache()

    df5 = df4.where(df4['diff']<0)
    df6 = df4.where(df4['diff']>0)

#   Find the count of clockwise and anticlockwise circles w.r.t countries

    df_cw_count = df5.groupby('countrycode').agg(functions.count('diff')).select(df5['countrycode'],functions.col('count(diff)').alias('cw_count'))
    df_acw_count = df6.groupby('countrycode').agg(functions.count('diff')).select(df6['countrycode'],functions.col('count(diff)').alias('acw_count'))


    df_join = df_cw_count.join(df_acw_count,df_cw_count['countrycode']==df_acw_count['countrycode']).select(df_cw_count['countrycode'],df_cw_count['cw_count'],df_acw_count['acw_count'],(df_cw_count['cw_count']+df_acw_count['acw_count']).alias('total_count'))

#   Find the percentage of CW and ACW circles for each country 

    df_final = df_join.select(df_join['countrycode'],((df_join['cw_count']/df_join['total_count'])*100).alias('cw_percentage'),((df_join['acw_count']/df_join['total_count'])*100).alias('acw_percentage'))
    df_final1 = df_final.orderBy(df_final['countrycode'],ascending=True)


#   Load the results into an intermediate collection to store dataset for applying classification models.
    df_final1.write.format("com.mongodb.spark.sql.DefaultSource").option("spark.mongodb.output.uri","mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.Insight8").mode("overwrite").save()

if __name__ == '__main__':
   main()

