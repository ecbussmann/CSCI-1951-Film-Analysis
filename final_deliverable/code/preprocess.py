import random
import pandas as pd
import numpy as np
import math

all_genres = ['Horror', 'Action', 'Adventure', 'Fantasy', 'Comedy', 'Crime', 'Drama', 'Mystery',
    'Sci-Fi', 'Thriller', 'Romance', 'Biography', 'Music', 'History', 'Animation', 'Sport',
    'War', 'Family', 'Musical', 'Western', 'Film-Noir']

def load_file1(file_path, x_var):
    """
    input:
        file_path: the path to the data file
        x_var:
            - for simple linear regression: the name of the independent variable
            - for multiple linear regression: a list of the names of the independent
            variables
            NOTE: to access a column in a pandas dataframe (df), you do
                    df['column_name'].values;
                to access multiple columns, you need df[['column_name1',
                    'column_name2', ..., ]]

    output:
        X: python list of independent variables values
        y: python list of the dependent variable
            values (i.e. 'cnt')
    """
    X, y = [],[] # placeholder values
    df = pd.read_csv('/Users/emilybelt/env/Final-Project/all_movies.csv')

    X1 = df[x_var].values.tolist()
    y1 = df["profit"].values.tolist()

    X = []
    y = []
    for item, i in zip(X1, list(range(len(X1)))):
        if not((math.isnan(item[5]))) and not((math.isnan(item[4]))) and not((math.isnan(item[3]))) and not((math.isnan(item[2]))) and not((math.isnan(item[0]))) and not(y1[i] == "FALSE") and (item[9] != ""):
            profit = int(item[1])
            item[1] = profit
            genres = (item[10].split(", "))
            item.pop(10)
            for j in all_genres:
                if j in genres:
                    item.append(1)
                else:
                    item.append(0)
            if item[3] >= 500:
                item[3] = 1
            else:
                item[3] = 0
            if item[4] >= 20:
                item[4] = 1
            else:
                item[4] = 0
            if item[5] >= 10:
                item[5] = 1
            else:
                item[5] = 0
            if "United States" in item[6].split(", "):
                item[6] = 1
            else:
                item[6] = 0
            if item[7] == "YES":
                item[7] = 1
            else:
                item[7] = 0
            if "en" !=  item[9].split(", "):
                item[9] = 1
            else:
                item[9] = 0
            month = item[8]
            item.pop(8)
            if (month == 12) or (month == 1) or (month == 2):
                item.append(1)
            else:
                item.append(0)
            if (3 <= month <= 5):
                item.append(1)
            else:
                item.append(0)
            if (6 <= month <= 8):
                item.append(1)
            else:
                item.append(0)
            if (9 <= month <= 11):
                item.append(1)
            else:
                item.append(0)
            X.append(item)
            y.append(int(y1[i]))
    return np.array(X), np.array(y)

def load_file2(file_path, x_var):
    X, y = [],[] # placeholder values
    df = pd.read_csv('/Users/emilybelt/env/Final-Project/all_movies.csv')

    X1 = df[x_var].values.tolist()
    y1 = df["mean_vote"].values.tolist()

    X = []
    y = []
    for item, i in zip(X1, list(range(len(X1)))):
        if not((math.isnan(item[5]))) and not((math.isnan(item[4]))) and not((math.isnan(item[3]))) and not((math.isnan(item[2]))) and not((math.isnan(item[0]))) and not(item[1] == "FALSE") and (item[9] != ""):
            profit = int(item[1])
            item[1] = profit
            
            genres = (item[10].split(", "))
            item.pop(10)
            for j in all_genres:
                if j in genres:
                    item.append(1)
                else:
                    item.append(0)
            if item[3] >= 500:
                item[3] = 1
            else:
                item[3] = 0
            if item[4] >= 20:
                item[4] = 1
            else:
                item[4] = 0
            if item[5] >= 10:
                item[5] = 1
            else:
                item[5] = 0
            if "United States" in item[6].split(", "):
                item[6] = 1
            else:
                item[6] = 0
            if item[7] == "YES":
                item[7] = 1
            else:
                item[7] = 0
            if "en" !=  item[9].split(", "):
                item[9] = 1
            else:
                item[9] = 0
            month = item[8]
            item.pop(8)
            if (month == 12) or (month == 1) or (month == 2):
                item.append(1)
            else:
                item.append(0)
            if (3 <= month <= 5):
                item.append(1)
            else:
                item.append(0)
            if (6 <= month <= 8):
                item.append(1)
            else:
                item.append(0)
            if (9 <= month <= 11):
                item.append(1)
            else:
                item.append(0)
            X.append(item)
            y.append(y1[i])
    return np.array(X), np.array(y)

def split_data_randomly(data, prob):
    """
    input:
    - data: a list of pairs of x,y values
    - prob: the fraction of the dataset that will be testing data, typically
    prob=0.2

    output:
    - a tuple of two lists with training data pairs and testing data pairs,
    respectively.
    """
    # placeholders - do not change this. first list: training data,
    # second list: testing data
    results = [], []
    # Split data randomly into fractions [prob, 1 - prob]. populate the lists
    # in the tuple
    for pt in data:
        random_num = random.random()
        if random_num < prob:
            #testing
            results[1].append(pt)
        else:
            #training
            results[0].append(pt)

    # return - you should not change this
    return results


def train_test_split(x, y, test_pct=0.2):
    """
    input:
        x: list of x values
        y: list of independent values
        test_pct: percentage of the data that is testing data (0.2 by default).

    output: x_train, x_test, y_train, y_test lists
    """
    # placeholders
    x_train, x_test, y_train, y_test = [], [], [], []
    # Split the features X and the labels y into x_train, x_test and
    # y_train, y_test as specified by test_pct

    pairs = zip(x, y)
    train, test = split_data_randomly(pairs, test_pct)
    x_train, y_train = zip(*train)
    x_test, y_test = zip(*test)

    # and then return :)
    return x_train, x_test, y_train, y_test
def calculate_r_squared(y_test, y_predicted):
    """
    Calculate the r-squared value

    Note: use the function R-Squared = 1 - SSE/SSTO

    input:
        y_test (list): the actual y values
        y_predicted (list): the predicted y values from the model

    output:
        r-squared (float)
    """
    r_squared_value = 0.0 # placeholder

    SSE = 0
    for test, pre in zip(y_test, y_predicted):
        SSE = SSE + (pre - test)*(pre - test)

    mean = 0
    for y in y_test:
        mean = mean + y/len(y_test)

    SSTO = 0
    for pt in y_test:
        SSTO = SSTO + (pt - mean)*(pt - mean)

    r_squared_value = 1 - (SSE/SSTO)
    return r_squared_value