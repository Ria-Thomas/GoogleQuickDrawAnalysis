# UNCOVERING TRENDS IN GOOGLE’S QUICKDRAW DATA  
Google’s Quick Draw is a simple application in which the user is instructed to draw an image in less than 20 seconds while a neural network predicts in real-time what the image represents. The Quick Draw Dataset is a collection of 50 million drawings across 345 categories, contributed by players of the game Quick, Draw!.  
  
## Objective:  
  
The objective of this project is to use the open-source data provided by Google for this application and put forward a collection of generic insights derived from this dataset along with the visualizations for the insights. We will also be using this dataset to determine the apt machine learning classification model that fits this data and plot the accuracy rates for each classifier.  
  
## About Dataset:  
  
The dataset that we are using as a part of the analysis is already pre-processed and is available in Simplified Drawing files (.ndjson) format. This file consists of the following attributes of the file:  

key_id - A unique identifier across all drawings.  
word - Category the player was prompted to draw.  
recognized - Whether the word was recognized by the game.  
timestamp - When the drawing was created.  
countrycode - A two-letter country code of where the player was located.  
drawing - A JSON array representing the vector drawing.
  
We are also using a few numpy bitmaps (.npy) which consists of simplified drawings that have been rendered into a 28x28 grayscale bitmap in numpy format for our Machine Learning Analysis.  
  
## Project Overview:  
  
The project involves trend analysis on the Google Quickdraw preprocessed dataset as well as various visualization based on the analysis performed. Here are the important elements of the project:  
  
1) Generic insights/Trends Analysis: Please find is a list of few insights we are generating from the analysis listed as below:  
	a) The most popular image in each country.  
	b) Images recognized correctly by application (distribution over percentages).  
	c) User engagement on the application wth respect to the time of the day.  
	d) Images not recognized by the application (distribution over percentages).  
	e) Relationship on the number of strokes used to draw an image by the user and the image being recognised as true.  
	f) Users of which country recognised a given image as true maximum number of times  
	g) What is the average number of strokes used for a given image by users of each country.  
	h) What percentage of users drew a "circle" image in Clockwise Direction or Anti-clockwise Direction.  
  
2) Machine Learning Analysis: It involves the computation of the model accuracy for the various classification algorithms mentioned below:  
	a) Random Forest Classifier.  
	b) K-Nearest Neighbour Classifier.  
	c) Decision Tree Classifier.  
	d) Gaussian naive bayes Classifier.  
	e) Multilayer Perceptron Classifier.  
  
3) visualization of the above data.  
  
All the visualization of the data in this project has been done using Tableau and some of the visualization snapshots can be found in [visualization](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/visualization/) folder in the project. We also have hosted the same tableau visualizations online in the link [here](https://public.tableau.com/profile/varnnitha#!/vizhome/CMPT732-BigDataTrio-GoogleQuickDrawInsights/FinalDash?publish=yes).  
  
## Here are the Steps to Execute in the Project:  
  
We are making use of the virtual machine (nml-cloud-13.cs.sfu.ca) part of the cluster for storing of the data and the Machine Learning Analysis. In order to run the generic insights mentioned above, we make use of the cluster. The dataset for the analysis can be downloaded from [here](https://www.kaggle.com/google/tinyquickdraw/download) and stored in the dataset folder. Please find more details on the same [here](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/RUNNING.txt).
  
## File Details:  
  
[mongoimport.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/db_loading_scripts/mongoimport.py)  
- populate the data into MongoDB using the mongoimport cmd line utility.  
  
[insight1.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight1.py)  
- generates insight of the most popular image at the country level.  
  
[insight2_4.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight2_4.py)  
- generates insight of images which the application guessed correctly the most or the least.  
  
[insight3.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight3.py)  
- generates insight on what time of the day people of which country are busy using this application.  
  
[insight5.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight5.py)  
- generates insight on the number of strokes used to draw an image by the user Vs image being recognized as true.  
  
[insight6.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight6.py)  
- generates insight on the user of which country recognized a given image as true maximum number of times.  
  
[insight7.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight7.py)  
- generates insight on the average number of strokes used for a given image by users of each country.  
  
[insight8.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/insight8.py)  
- generates insight on the percentage of users who drew a "circle" image in the Clockwise Direction or Anti-clockwise Direction.  
  
[run_insights.sh](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/run_insights.sh)  
- this file can be used to run all the insights in one shot or even each of the insights one by one.  
  
[insight_ml1.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/insight_ml1.py)  
- this file does the classification on the data using Random Forest Classifier.  
  
[insight_ml2.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/insight_ml2.py)  
- this file does the classification on the data using K-Nearest Neighbour Classifier.  
  
[insight_ml3.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/insight_ml3.py)  
- this file does the classification on the data using the Decision Tree Classifier.  
  
[insight_ml4.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/insight_ml4.py)  
- this file does the classification on the data using the Gaussian Naive Bayes Classifier.  
  
[run_classifier.sh](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/run_classifier.sh)  
- this file can be used to run all the Classifiers or even individual classification as mentioned above.  
  
[load_ml_data.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/load_ml_data.py)  
- this file loads the required data that needed for running all of the above-mentioned ML models.  
  
[ML_All_Comparison.py](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/ML_All_Comparison.py)  
- this file makes use of two .npy files to run the classification algorithm on 4 different ML classifiers: MLP, RandomForest, DecisionTree, NaiveBayes.  
  
## Folders:  
  
[db_loading_scripts](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/db_loading_scripts/)  
- this folder contains all the datasets used for the project.  
  
[insight_analysis](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/insight_analysis/)  
- this folder contains files that are used to generate the generic set of insights in the project.  
  
[machine_learning_analysis](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/machine_learning_analysis/)  
- this folder contains files that do the machine learning analysis for the various alogrithms included above.  
  
[visualization](https://csil-git1.cs.surrey.sfu.ca/asundarr/bigdata1project/blob/master/visualization/)  
- this folder contains the snapshots of the visualizations performed in the project.
