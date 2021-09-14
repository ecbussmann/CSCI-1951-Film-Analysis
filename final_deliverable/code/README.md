# Code README
This is where you can document your design decisions, known bugs, and instructions to run your code.

### Regression Model ###
The preproccess.py and regression.py are the two files we use to conduct our regression.
The preproccess.py processes the dataset; it adds independent variables and dependent variables that 
fulfill certain requirements (i.e. have no null values) to new X and y lists. It also processes the independent variables to be of the right form; 
for example, we change genres, country of production, popular directors, writers, and production companies, release season, and 
language into indicator variables. We then return these X and y lists to be used to create our models in regression.py.
In regression.py, we split our data 80/20 processes by preproccess.py into testing and training data. We then build a regression using
the training data and test the model by returning the R-Squared and MSE values of the model on the testing data. We print out the regression report as well as
the testing R-Squared and MSE values.
In regression.py, we build two regression models: one to predict mean vote and one to predict profit. 
To run the profit model, set x, y to load_file1 with x_var1 as the second input.
To run the mean vote model, set x, y to load_file2 with x_var2 as the second input.
The first input in both of the load_file functions from preprocess.py is the path to the all_movies.csv dataset.
The csv file we used to run this model is slightly different than the one in our dataset; we added three columns to assist in the regression.
The first column (director_count) counts the number of times the respective director appears in the dataset, 
the second column (writer_count) counts the number of times the respective writer appears in the dataset,
and the third column (production_count) counts the number of times the respective productiion company appears in the dataset. 
These counts are used to determine if the movie was directed by, written by, or produced by a popular director, writter, or production company. 
These figures with counts above certain thresholds are considered popular.
This csv file with the three added columns can be found in our code section under all_movies.zip (we compressed it due to the size of the csv file). 
The path to this csv should be used for the first input of the load_file functions.

### Naive Bayesian Classifiers ###
The naive_bayes.py file is the file we used to run our Naive Bayesian
Classifier algorithms. In the main function, it runs four Naive Bayesian
Classifiers based on average mean rating, average profit, 70th percentile
of mean rating, and 70th percentile of profit (we only actually utilized 
the latter two in the results of our final project). For each classifier, it
prints out information such as the threshold for success (movies above
that threshold are labeled as "successful", with Y=1, and movies below
are labeled as "unsuccessful", with Y=0), the number of movies in the
training and testing datasets, the probability that a movie is successful
(equivalent to the proportion of all movies that are above the threshold),
the accuracy rate, the false positive rate, and the false negative rate.
In the main function, there is also the execution of 18 Naive Bayes
Classifiers--9 classifiers for 9 different percentile thresholds of mean
vote and 9 classifiers for 9 different percentile thresholds of profit.
This data is stored into a csv elsewhere in this project repository.

The implementation of our Naive Bayesian Classifier (which was used
for each execution of a Naive Bayesian Classifier) is as follows:
1) The relevant data is obtained in the get_data() function 
   from the large metadata and keywords
CSV files based on the movie success metric we are currently using 
   (average user rating or profit). This data is stored into two
   dataframes, one with the movie ID and movie success metric values
   and the other with the movie ID and the associated keywords.
   
2) The two dataframes are then joined in the join_tables() function
   such that there is a single 
joined dataframe, where each row/tuple is: (movie ID, movie success 
   metric, keyword).
   
3) Next, depending on the type of threshold, the calc_threshold (for
   average thresholds) or calc_pctile (for percentile thresholds) 
   function is called, in which movies are only accounted for once--duplicates
   of the same movie are temporarily dropped--and the threshold is calculated.
   
4) Movies are then labeled as being above (Y=1) or below (Y=0) the 
threshold in the label_above_below_threshold() function.
   
5) The data is split 80/20 into training/testing data, respectively,
in the split_train_test() function. We wanted to keep movies together
   (i.e., avoid splitting up a movie such that some of the keyword/movie pairs
   for a single movie are in the training set and the rest of the pairs are
   in the testing set). This function returns the movie IDs and the
   corresponding Ys (Y=0 or 1)
   and lists of keywords for movies, separated by whether movies are in
   the training set or the testing set.
   
6) The probability that a movie is successful (equivalently, that Y=1 and
   that the movie is above the threshold) is calculated in the function
   get_pY(), which calculates this probability 
   using only the movies in the training set.
   
7) The conditional probabilities that a word is in a movie, given that it
is successful or not (P(word | Y)) is calculated for each word in the function
   calc_cond_ps(), using only the training data.
   
8) Predictions are made for the movies in the testing data based on
the keywords associated with those movies in the predict() function.
   In this function, for each movie, two conditional probabilities are
   calculated: the probability that the movie will be successful conditional
   on its keywords (P(Y=1 | words)), and the probability that the movie
   will be unsuccessful conditional on its keywords (P(Y=0 | words)). 
   The movie is then classified based on which conditional probability is
   greater.
   
9) Lastly, the success metrics for the Classifier are calculated in the
get_accuracy() function, which calculates the accuracy rate, the false
   positive rate, and the false negative rate.
   
In order to run this file, from the terminal, one can simply write the
command: python3 naive_bayes.py

As far as we know, there are no significant bugs in this code, however,
given that we did not explicitly study an implementation for this machine
learning technique (unlike how we did for K-means and single and multiple
regression), we felt it would be important to include in our final project
deliverable in case any errors were made.

For more ways to organize your report, check this markdown cheatsheet: https://github.com/tchapi/markdown-cheatsheet/blob/master/README.md

We ***highly encourage you to use markdown syntax to organize and clean your reports*** since it will make it a lot more comprehenisble for the TA grading your project.
