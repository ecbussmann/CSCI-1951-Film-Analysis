import pandas as pd
import numpy as np
import random

SPLIT = '|||'
P_NONE = 0.00001
PERCENTILE = 0.7

Y_VAR1 = 'mean_vote'
Y_VAR2 = 'profit'

def get_data(movies_file_path, kw_file_path, Y_var):
    movies_df = pd.read_csv(movies_file_path)
    movies_df = movies_df[['id', Y_var]]
    if Y_var == Y_VAR2:
        movies_df = movies_df[movies_df[Y_var] != 'FALSE']
        movies_df[Y_var] = movies_df[Y_var].astype(int)
    return movies_df, pd.read_csv(kw_file_path)

def join_tables(movies_df, kw_df, Y_var):
    # join based on movie_id
    movies_df.columns = ['movie_id', Y_var]
    joined_df = kw_df.set_index('movie_id').join(movies_df.set_index('movie_id'))
    joined_df.dropna(inplace=True)
    joined_df.reset_index(inplace=True)
    return joined_df

def calc_threshold(movies_df, Y_var):
    # remove duplicates for calculating the threshold -- we don't want
    # to count a movie's rating or profit more than once in this calculation
    movies_df.drop_duplicates(subset='movie_id', inplace=True)
    movies_df.reset_index(inplace=True)
    all_ratings = movies_df[Y_var]
    threshold = np.mean(np.array(all_ratings))
    print("    Threshold: ", threshold)
    return threshold

def calc_pctile(movies_df, Y_var, percentile):
    if percentile == 0.00:
        all_ratings = [1] * len(Y_var)
    else:
        all_ratings = movies_df[Y_var]
    threshold = np.quantile(np.array(all_ratings), percentile)
    print("    Percentile: ", percentile)
    print("    Threshold: ", threshold)
    return threshold

def label_above_below_threshold(movies_df, avg_avg_rating, Y_var):
    movies_df['Y'] = (movies_df[Y_var] > avg_avg_rating)
    movies_df.loc[movies_df['Y'] == True, 'Y'] = 1
    movies_df.loc[movies_df['Y'] == False, 'Y'] = 0
    del movies_df[Y_var]
    return movies_df

def split_train_test(df, test_pct=0.2):
    # split movies based on the id (we don't want to split up movies
    # between training and testing data)
    train_ids = []
    test_ids = []
    train_Ys = []
    test_Ys = []
    train_words = []
    test_words = []
    df.sort_values(by=['movie_id'], inplace=True)
    ids = list(df['movie_id'])
    Ys = list(df['Y'])
    words = list(df['word'])
    prev_id = None
    prev_type = ""
    curr_index_train = None
    curr_index_test = None
    for i in range(len(ids)):
        id = ids[i]
        Y = Ys[i]
        word = words[i]
        if id != prev_id:
            if random.random() <= test_pct: # becomes part of testing data
                if curr_index_test == None:
                    curr_index_test = 0
                else:
                    curr_index_test = curr_index_test + 1
                test_ids.append(id)
                test_Ys.append(Y)
                test_words.append(word + SPLIT)
                prev_type = 'test'
            else:
                if curr_index_train == None:
                    curr_index_train = 0
                else:
                    curr_index_train = curr_index_train + 1
                train_ids.append(id)
                train_Ys.append(Y)
                train_words.append(word + SPLIT)
                prev_type = 'train'
            prev_id = id
        else:
            if prev_type == 'test':
                test_words[curr_index_test] = test_words[curr_index_test] + word + SPLIT
            else:
                train_words[curr_index_train] = train_words[curr_index_train] + word + SPLIT
    print("    Number of training data points: ", len(train_ids))
    print("    Number of testing data points: ", len(test_ids))
    return train_ids, test_ids, train_Ys, test_Ys, train_words, test_words


def get_pY(train_Ys): # should be computed from the training data
    pY = np.mean(np.array(train_Ys))
    print("    Probability that Y=1: ", pY)
    return pY

def calc_cond_ps(words, Ys):
    words_y1 = {} # {word: count}
    num_y1 = 0
    words_y0 = {} # {word: count}
    num_y0 = 0
    for i in range(len(words)):
        words_list = words[i].split(SPLIT)
        for word in words_list:
            if Ys[i] == 1:
                num_y1 = num_y1 + 1
                if word in words_y1:
                    words_y1[word] = words_y1[word] + 1
                else:
                    words_y1[word] = 1
            else:
                num_y0 = num_y0 + 1
                if word in words_y0:
                    words_y0[word] = words_y0[word] + 1
                else:
                    words_y0[word] = 1
    # change the values into conditional probabilities: P(word | Y)
    # = P(word and Y) / P(Y)
    # words_y1[wordi] = number of words that satisfy word = wordi and Y=1
    for word in words_y1:
        words_y1[word] = words_y1[word] / num_y1
    for word in words_y0:
        words_y0[word] = words_y0[word] / num_y0
    # words_y1 = {word: P(word | Y=1)}
    return words_y1, words_y0

def predict(pY1, cond_Y1, cond_Y0, ids, words):
    pY0 = 1 - pY1
    predictions = []
    for i in range(len(ids)):
        # calculate P(Y=1 | words) and P(Y=0 | words)
        pred_Y1 = pY1
        pred_Y0 = pY0
        words_list = words[i].split(SPLIT)
        for word in words_list:
            if word in cond_Y1:
                pred_Y1 = pred_Y1 * (cond_Y1[word])
            else:
                pred_Y1 = pred_Y1 * P_NONE
            if word in cond_Y0:
                pred_Y0 = pred_Y0 * (cond_Y0[word])
            else:
                pred_Y0 = pred_Y0 * P_NONE
        # whichever one is bigger: that is the classification given by the algorithm
        if pred_Y1 >= pred_Y0:
            predictions.append(1)
        else:
            predictions.append(0)
    return predictions

def get_accuracy(Ys, pred_Ys):
    correct = 0
    false_pos = 0
    false_neg = 0
    true_pos = 0
    true_neg = 0
    for i in range(len(Ys)):
        if Ys[i] == pred_Ys[i]:
            correct = correct + 1
        elif Ys[i] == 0 and pred_Ys[i] == 1:
            false_pos = false_pos + 1
        elif Ys[i] == 1 and pred_Ys[i] == 0:
            false_neg = false_neg + 1
    true_pos = np.sum(np.array(Ys))
    true_neg = len(Ys) - true_pos
    accuracy = correct / len(Ys)
    false_pos_rate = false_pos / (false_pos + true_neg)
    false_neg_rate = false_neg / (false_neg + true_pos)
    print("    Accuracy: ", accuracy)
    print("    False positive rate (predict Y=1 when Y=0): ", false_pos_rate)
    print("    False negative rate (predict Y=0 when Y=1): ", false_neg_rate)
    return accuracy, false_pos_rate, false_neg_rate

def y_avg_mean_rating(movies_file_path, kw_file_path, y):
    print('Average mean rating:')
    movies_df, kw_df = get_data(movies_file_path, kw_file_path, y)
    # join the data
    joined_df = join_tables(movies_df, kw_df, y)
    avg_avg_rating = calc_threshold(joined_df, y)
    joined_df = label_above_below_threshold(joined_df, avg_avg_rating, y)

    # split data here and only use training data to find conditional probabilities
    train_ids, test_ids, train_Ys, test_Ys, train_words, test_words = split_train_test(joined_df)

    # use only training data to calculate initial conditional probabilities
    pY1 = get_pY(train_Ys)
    cond_pY1, cond_pY0 = calc_cond_ps(train_words, train_Ys)

    # test with testing data
    predictions = predict(pY1, cond_pY1, cond_pY0, test_ids, test_words)
    accuracy, false_pos, false_neg = get_accuracy(test_Ys, predictions)

def y_avg_profit(movies_file_path, kw_file_path, y):
    print('Average profit:')
    movies_df, kw_df = get_data(movies_file_path, kw_file_path, y)
    # join the data
    joined_df = join_tables(movies_df, kw_df, y)
    avg_profit = calc_threshold(joined_df, y)
    joined_df = label_above_below_threshold(joined_df, avg_profit, y)

    # split data here and only use training data to find conditional probabilities
    train_ids, test_ids, train_Ys, test_Ys, train_words, test_words = split_train_test(joined_df)

    # use only training data to calculate initial conditional probabilities
    pY1 = get_pY(train_Ys)
    cond_pY1, cond_pY0 = calc_cond_ps(train_words, train_Ys)

    # test with testing data
    predictions = predict(pY1, cond_pY1, cond_pY0, test_ids, test_words)
    accuracy, false_pos, false_neg = get_accuracy(test_Ys, predictions)

def y_pctile_mean_rating(movies_file_path, kw_file_path, y):
    print('Percentile mean rating:')
    movies_df, kw_df = get_data(movies_file_path, kw_file_path, y)
    # join the data
    joined_df = join_tables(movies_df, kw_df, y)
    pctile_avg_rating = calc_pctile(joined_df, y, PERCENTILE)
    joined_df = label_above_below_threshold(joined_df, pctile_avg_rating, y)

    # split data here and only use training data to find conditional probabilities
    train_ids, test_ids, train_Ys, test_Ys, train_words, test_words = split_train_test(joined_df)

    # use only training data to calculate initial conditional probabilities
    pY1 = get_pY(train_Ys)
    cond_pY1, cond_pY0 = calc_cond_ps(train_words, train_Ys)

    # test with testing data
    predictions = predict(pY1, cond_pY1, cond_pY0, test_ids, test_words)
    accuracy, false_pos, false_neg = get_accuracy(test_Ys, predictions)

def y_pctile_profit(movies_file_path, kw_file_path, y):
    print('Percentile profit:')
    movies_df, kw_df = get_data(movies_file_path, kw_file_path, y)
    # join the data
    joined_df = join_tables(movies_df, kw_df, y)
    pctile_avg_rating = calc_pctile(joined_df, y, PERCENTILE)
    joined_df = label_above_below_threshold(joined_df, pctile_avg_rating, y)

    # split data here and only use training data to find conditional probabilities
    train_ids, test_ids, train_Ys, test_Ys, train_words, test_words = split_train_test(joined_df)

    # use only training data to calculate initial conditional probabilities
    pY1 = get_pY(train_Ys)
    cond_pY1, cond_pY0 = calc_cond_ps(train_words, train_Ys)

    # test with testing data
    predictions = predict(pY1, cond_pY1, cond_pY0, test_ids, test_words)
    accuracy, false_pos, false_neg = get_accuracy(test_Ys, predictions)

if __name__=='__main__':
    movies_file_path = 'Data/all_movies_table.csv'
    kw_file_path = 'Data/keywords.csv'
    y_avg_mean_rating(movies_file_path, kw_file_path, Y_VAR1)
    y_avg_profit(movies_file_path, kw_file_path, Y_VAR2)
    y_pctile_mean_rating(movies_file_path, kw_file_path, Y_VAR1)
    y_pctile_profit(movies_file_path, kw_file_path, Y_VAR2)