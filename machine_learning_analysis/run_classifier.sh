#
# History of the file
#*********************
#
# Dec 04 2019 - creation - asundarr
# 
# PreRequisite: please ensure if you are running this code on the VM provided to the team nml-cloud-13.cs.sfu.ca.
#

#!/usr/bin/bash 
usage()  
{  
 echo "Usage: $0 [ALL|Random_Forest|KNN|Decision_Tree|Gaussian_NB]"
 exit 1  
} 

if [ $# -ne 1 ] ; then
    usage
else
    filename=$1
fi

case $filename in
   "Random_Forest")
        echo "We are running Random Forest Classifier on the Google Quick Draw Dataset."
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml1.py ;;
   "KNN")
        echo "We are running K-Nearest Neighbour Classifier on the Google Quick Draw Dataset."
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml2.py ;;
   "Decision_Tree")
        echo "We are running Decision Tree Classifier on the Google Quick Draw Dataset."
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml3.py ;;
   "Gaussian_NB")
        echo "We are running Gaussian naive bayes Classifier on the Google Quick Draw Dataset."
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml4.py ;;
   "ALL")
        echo "We are running All the 4 classification alogorithm on the data"
        echo "############# Random Forest Classifier ###############"
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml1.py
        echo "############# K-Nearest Neighbour Classifier ###############"
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml2.py
        echo "############# Decision Tree Classifier ###############"
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml3.py
        echo "############# Gaussian naive bayes Classifier ###############"
        ${SPARK_HOME}/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight_ml4.py ;;
   *) 
        echo "wrong option provided to run the script";;
esac
