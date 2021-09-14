import numpy as np
import csv
from statsmodels.tools import eval_measures
import random
import math
from preprocess import train_test_split, load_file, load_file2, calculate_r_squared

class SimpleLinearRegression:

    #TODO: Implement Simple Linear Regression
    def mean(self, values):
        """
        Input:
        - values: A list of values
        Output:
        - One value, that is the mean of the list. Can be of type float,
        or numpy float!
        """
        mean = 0.0 # placeholder value
        n = len(values)
        for v in values:
            mean = mean + v/n
        # and return
        return mean


    def variance(self, values, mean):
        """
        Inputs:
        - values: A list of values
        - mean: The mean of the list /values/
        Output:
        - One value, that is the variance of the list. Can be of type float,
        or numpy float!
        """
        var = 0.0 # placeholder value
        # use n-1 as denominator
        denom = len(values) - 1
        for v in values:
            var = var + (v - mean)*(v - mean)/denom
        # and return
        return var


    def covariance(self, X, y, mean_X, mean_y):
        """
        Inputs:
        - X, y: lists of values
        - mean_X, mean_y: Means of X and y
        Output:
        - One value, that is the covariance of X and y. Can be of type float,
        or numpy float!
        """
        covar = 0.0 # placeholder value
        # use n-1 as denominator
        denom = len(y) - 1
        for x1,y1 in zip(X,y):
            covar = covar + (x1 - mean_X)*(y1 - mean_y)/denom

        # and return
        return covar


    def train_regression(self,X,y):
        """
        This is where you implement simple linear regression.
        Inputs:
        - X, y: lists of values
        Output:
        - a, b: The coefficients of the model << y = a + b*x >>. Floats or
        numpy floats.
        """
        a, b = 0.0, 0.0
        # TODO: Calculate and return the coefficients (a, b) of the the model,
        # y = a + b*x.
        mean_x = self.mean(X)
        mean_y = self.mean(y)
        b = self.covariance(X, y, mean_x, mean_y)/self.variance(X, mean_x)
        a = mean_y - b*mean_x
        # and return. DO NOT modify the order of returns.
        return a, b


    def test_regression(self, X_train, X_test, y_train, y_test, a, b):
        """
        This is where you calculate and print
            - training R-squared
            - training MSE
            - testing MSE
        Inputs:
        - X_train, y_train, X_test, y_test: lists of training and testing values
        - a, b: coefficients (of the model << y = a + b*x >> that are
        identified using train_regression)
        Outputs:
        - The Mean Squared Error value when applying the model on the training
        dataset (training_MSE)
        - The Mean Squared Error value when applying the model on the testing
        dataset (testing_MSE)
        - The R-Squared value when applying the model on the *testing* dataset
        (testing_R2)
        """
        # placeholder values
        training_MSE, testing_MSE, testing_R2 = 0.0, 0.0, 0.0

        train_results = list(map(lambda x: x*b + a, X_train))
        training_MSE = eval_measures.mse(train_results, y_train)

        test_results = list(map(lambda x: x*b + a, X_test)) # predicted
        testing_MSE = eval_measures.mse(y_test, test_results)

        testing_R2 = calculate_r_squared(y_test, test_results)

        # print out the values
        #print("Training MSE: ", training_MSE)
        #print("Testing MSE: ", testing_MSE)
        #print("Testing R-Squared: ", testing_R2)
        # and then return, woohoo! -- pls don't change the order of returns.
        return training_MSE, testing_MSE, testing_R2


if __name__=='__main__':
    # DO not change this seed. It guarantees that all students perform the same
    # train and test split
    random.seed(1)
    model = SimpleLinearRegression()

    # Call load_file; x_var should be a string for the column name
    x_var = ['popular_actors','runtime', 'series', 'genre', 'month', 'country', 'director', 'production_company', 'profit', 'mean_vote']
    x_var2 = ['popular_actors','runtime', 'month']

    #x_var = ['profit', 'mean_vote']
    # instead get xvars and yvars as matrix and just do
    # have it just return the x?
    # x is going to be a list of lists
    indep = load_file2("Data/all_movies_table.csv", x_var)
    num_rows = len(indep)
    #print(indep[num_rows - 1])
    num_vars = len(x_var)

    count = 0
    for i in range(num_vars):
        for j in range(num_vars):
            if i != j:
                x = indep[:,i]
                y = indep[:,j]
                print(x)
                print(y)
                x_train, x_test, y_train, y_test = train_test_split(x, y)
                a, b = model.train_regression(x_train, y_train)
                training_MSE, testing_MSE, testing_R2 = model.test_regression(x_train, x_test, y_train, y_test, a, b)
                print(str(i) + ", " + str(j) + ": " + str(testing_R2))
    count = count + 1

    # Use train test split to split data into x_train, x_test, y_train,
    # y_test
    #x_train, x_test, y_train, y_test = train_test_split(x, y)

    # Train and test linear regression model
    #a, b = model.train_regression(x_train, y_train)
    #print (b)
    #training_MSE, testing_MSE, testing_R2 = model.test_regression(x_train, x_test, y_train, y_test, a, b)
