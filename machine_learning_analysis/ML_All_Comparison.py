#
# This file comparing 4 different ML classifiers : MLP, RandomForest, DecisionTree, NaiveBayes
# 
# Here is the way to run the file: ${SPARK_HOME}/bin/spark-submit ML_All_Comparison.py 
#
#
# History of the file
#*********************
#
# Nov 24 2019 - Creation - riat
# Nov 29 2019 - Edited the code and did some code formatting to remove unwanted definitons - asundarr

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import numpy as np
from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('ml code').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
assert spark.version >= '2.4' # make sure we have Spark 2.4+

from pyspark.ml.classification import MultilayerPerceptronClassifier,RandomForestClassifier,DecisionTreeClassifier,NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vectors

def main():

    cat = np.load('/home/ubuntu/dataset/cat.npy')
    cow = np.load('/home/ubuntu/dataset/cow.npy')

###########################################################################
# ADD COLUMNS OF 0 AND 1 TO THE FEATURE MATRICES AS THE CLASS LABELS
###########################################################################
    cat = np.c_[np.zeros(len(cat)),cat]
    cow = np.c_[np.ones(len(cow)),cow]

###########################################################################
# TAKE SAME NUMBER OF SAMPLES FROM BOTH CLASSES AND CONCATENATE THEM
###########################################################################

    X = np.concatenate((cat[:5000,],cow[:5000,]), axis=0).astype('float32')

###########################################################################
# CREATE DENSE VECTORS FOR THE FEATURES AND CONVERT THEM TO A DATAFRAME
###########################################################################
    dff = map(lambda x: (int(x[0]), Vectors.dense(x[1:])), X)
    mydf = spark.createDataFrame(dff,schema=["label", "features"])

###########################################################################
# SPLIT THE INPUT DATAFRAME INTO TRAININGING AND TESTING DATA
###########################################################################

    train, validation = mydf.randomSplit([0.75, 0.25])

###########################################################################
# DEFINE MODEL, TRAIN THE MODEL AND PERFORM VALIDATION
###########################################################################

###########################################################################
# MULTILAYER PERCEPTRON
###########################################################################

    mlp = MultilayerPerceptronClassifier(maxIter=100, layers=[784, 100, 2], blockSize=1, seed=123)
    model1 = mlp.fit(train)

    dataset1 = model1.transform(validation)
    evaluator1 = MulticlassClassificationEvaluator(predictionCol="prediction")
    score1 = evaluator1.evaluate(dataset1,{evaluator1.metricName: "accuracy"})
	
    print('Validation score for Multilayer Perceptron model: %g' % (score1, ))

###########################################################################
# RANDOM FOREST
###########################################################################

    rf = RandomForestClassifier(numTrees=3, maxDepth=2, labelCol="label", seed=42)
    model2 = rf.fit(train)

    dataset2 = model2.transform(validation)
    evaluator2 = MulticlassClassificationEvaluator(predictionCol="prediction")
    score2 = evaluator2.evaluate(dataset2,{evaluator2.metricName: "accuracy"})
	
    print('Validation score for Random Forest model: %g' % (score2, ))

###########################################################################
# DECISION TREE
###########################################################################

    dt = DecisionTreeClassifier(maxDepth=2, labelCol="label")
    model3 = dt.fit(train)

    dataset3 = model3.transform(validation)
    evaluator3 = MulticlassClassificationEvaluator(predictionCol="prediction")
    score3 = evaluator3.evaluate(dataset3,{evaluator3.metricName: "accuracy"})
	
    print('Validation score for Decision tree model: %g' % (score3, ))

###########################################################################
# NAIVE BAYES
###########################################################################

    nb = NaiveBayes(smoothing=1.0, modelType="multinomial")
    model4 = nb.fit(train)

    dataset4 = model4.transform(validation)
    evaluator4 = MulticlassClassificationEvaluator(predictionCol="prediction")
    score4 = evaluator4.evaluate(dataset4,{evaluator4.metricName: "accuracy"})
	
    print('Validation score for Naive Bayes model: %g' % (score4, ))

if __name__ == '__main__':
   main()


