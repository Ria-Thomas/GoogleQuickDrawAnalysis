#
# This file is used for Using Gaussian naive bayes Classification
# The insight of providing the details of Using Gaussian naive bayes Classification on the given dataset interms pediction for the dataset.
# 
# Here is the way to run the file: ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml4.py
#

#
# History of the file
#*********************
#
# Nov 24 2019 - creation - asundarr
# Nov 29 2019 - Code formatting and edited the mongdb collection - riat
# Dec 03 2019 - code revisit - asundarr
# 

import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import com.mongodb
from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.config('spark.mongodb.input.uri','mongodb://nml-cloud-13.cs.sfu.ca:27017/BigDataTrio.MLData').getOrCreate()
assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')

def main():
   df_word1 = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

   df_model_inputs = df_word1.select(df_word1['drawing2[0]'], df_word1['drawing2[1]'], df_word1['drawing2[2]'], df_word1['drawing2[3]'], df_word1['drawing2[4]'], df_word1['drawing2[5]'], df_word1['drawing2[6]'], df_word1['drawing2[7]'], df_word1['drawing2[8]'], df_word1['drawing2[9]'], df_word1['drawing2[10]'], df_word1['drawing2[11]'], df_word1['drawing2[12]'], df_word1['drawing2[13]'], df_word1['drawing2[14]'], df_word1['drawing2[15]'], df_word1['drawing2[16]'], df_word1['drawing2[17]'], df_word1['drawing2[18]'], df_word1['drawing2[19]'], df_word1['drawing2[20]'], df_word1['drawing2[21]'], df_word1['drawing2[22]'], df_word1['drawing2[23]'], df_word1['drawing2[24]'], df_word1['drawing2[25]'], df_word1['drawing2[26]'], df_word1['drawing2[27]'], df_word1['drawing2[28]'], df_word1['drawing2[29]'], df_word1['drawing2[30]'],  df_word1['drawing2[31]'], df_word1['drawing2[32]'], df_word1['drawing2[33]'], df_word1['drawing2[34]'], df_word1['drawing2[35]'], df_word1['drawing2[36]'], df_word1['drawing2[37]'], df_word1['drawing2[38]'], df_word1['drawing2[39]'], df_word1['recognized'])   

   data = df_model_inputs.toPandas()

   dataset = data.iloc[:, 0:39]
   labels = data.iloc[:, 40]

   x_data_train, x_data_test, y_label_train, y_label_test = train_test_split(dataset, labels, test_size=0.3, random_state=2)

   print("Using Gaussian naive bayes Classification")

   # Choosing the model for the classification of the data
   model = GaussianNB()

   # Fitting the data to the model
   model.fit(x_data_train, y_label_train)
   	
   Label_pred = model.predict(x_data_test)

   # Confusion Matrix to give us the idea on TP, TN, FP, FN in the model prediction.
   print("Confusion matrix for the Gaussian naive bayes Classification")
   print(confusion_matrix(y_label_test, Label_pred)) 

   # Classification report for the model in general
   print("Classification report")
   print(classification_report(y_label_test, Label_pred)) 

if __name__ == '__main__':
   main()	
