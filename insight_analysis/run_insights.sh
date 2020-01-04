#
# History of the file
#*********************
#
# Dec 03 2019 - creation - asundarr
# 
# PreRequisite: Ensure if you are running this code on gateway that the #module load spark command is run.
#

#!/usr/bin/bash 
usage()  
{  
 echo "Usage: $0 [ALL|insight1|insight2_4|insight3|insight5|insight6|insight7|insight8]"  
 exit 1  
} 

if [ $# -ne 1 ] ; then
    usage
else
    filename=$1
fi

case $filename in
   "insight1") 
	echo "Running Insight 1 - providing the details of which images are the most popular ones in each of the 207 countries."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight1.py ;;
   "insight2_4")
        echo "Running Insight 2 & 4 combined - providing the details of the images which the application guessed correctly the most or the least in terms of percentage."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight2_4.py ;;
   "insight3")
	echo "Running Insight 3 - providing the details of what time of the day people of which country are busy using this application."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight3.py ;;
   "insight5")
	echo "Running Insight 5 - providing the details of comparison of the number of strokes vs correctness of the guess in percentage."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight5.py ;;
   "insight6")
	echo "Running Insight 6 - providing the details of which country recognised a given image correctly maximum number of times."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight6.py ;;
   "insight7")
	echo "Running Insight 7 - providing the details of avg number of strokes drawn by each country for a particular object."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight7.py ;;
   "insight8")
	echo "Running Insight 8 - providing the details of a circle image in particular whether it was drawn in clockwise direction or anti-clockwise direction."
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight8.py ;;
   "ALL")
	echo "Running All the Insights one by one."
        echo "######## Insight 1 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight1.py
        echo "######## Insight 2 and 4 combined ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight2_4.py 
        echo "######## Insight 3 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight3.py
        echo "######## Insight 5 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight5.py
        echo "######## Insight 6 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight6.py
        echo "######## Insight 7 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight7.py
        echo "######## Insight 8 ########"
        spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1 insight8.py ;;
   *) 
        echo "wrong option provided to run the script";;
esac
