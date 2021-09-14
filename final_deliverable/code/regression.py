import numpy as np
import random
import statsmodels.api as sm
from statsmodels.tools import eval_measures
from preprocess import train_test_split, load_file1, load_file2, calculate_r_squared
import sqlite3

def multiple_regression(X_train, X_test, y_train, y_test):
    """
    A multiple linear regression using StatsModel
    Inputs:
    - X_train, X_test, y_train, y_test: lists of training and testing values

    Outputs:
    - The Mean Squared Error value when applying the model on the training
    dataset (training_MSE)
    - The Mean Squared Error value when applying the model on the testing
    dataset (testing_MSE)
    - The R-Squared value when applying the model on the *testing* dataset
    (testing_R2)
    """
    # Placeholder - your function should update these three variables and
    # return the correct values for these three variables!
    training_MSE, testing_MSE, testing_R2 = 0, 0, 0

    # TODO: Use StatsModels to create the Linear Model and Output R-squared
    #X_train = np.array(X_train).astype(np.float)
    X_train = sm.add_constant(X_train)
    X_test = sm.add_constant(X_test)

    ols_model = sm.OLS(y_train, X_train)
    res = ols_model.fit()

    train_predictions = res.predict(X_train)
    test_predictions = res.predict(X_test)

    training_MSE = eval_measures.mse(train_predictions, y_train)
    testing_MSE = eval_measures.mse(test_predictions, y_test)
    testing_R2 = calculate_r_squared(y_test, test_predictions)
    residuals1 = []
    for i, j in zip(y_test, test_predictions):
        residuals1.append(i - j)
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS "residuals";')
    c.execute('CREATE TABLE residuals(predict FLOAT, residual FLOAT);')
    conn.commit()

    for i, j in zip(test_predictions, residuals1):
        c.execute('''INSERT INTO residuals VALUES (?, ?);''', (i, j))
    conn.commit()

    print(res.summary())
    print("Testing R-Squared: ", testing_R2)
    print("Training MSE: ", training_MSE)
    print("Testing MSE: ", testing_MSE)
    # return
    return training_MSE, testing_MSE, testing_R2



if __name__=='__main__':

    # DO not change this seed. It guarantees that all students perform the same
    # train and test split
    random.seed(1)

    # include significant variables that maximize r-squared
    x_var1 = ['runtime', 'mean_vote', 'popular_actors', 'production_count', 'director_count', 'writer_count', 'country', 'series', 'month', 'original_language', 'genre']
    x_var2 = ['runtime', 'profit', 'popular_actors', 'production_count', 'director_count', 'writer_count', 'country', 'series', 'month', 'original_language', 'genre']


    x, y = load_file2("/Users/emilybelt/env/Final-Project/all_movies.csv", x_var2)
    num_rows = len(y)
    #x, y = np.array(x), np.array(y)

    # split data
    x_train, x_test, y_train, y_test = train_test_split(x, y)

    # run regression
    training_MSE, testing_MSE, testing_R2 = multiple_regression(x_train, x_test, y_train, y_test)
