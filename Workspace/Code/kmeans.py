import numpy as np
import random
import math
import matplotlib.pyplot as plt
import pandas as pd


MAX_K = 10
MAX_ITER = 500

def get_data(file_path, vars):
    df = pd.read_csv(file_path)[vars]
    if 'series' in vars:
        df['series'] = (df['series'] == 'YES').astype(int)
    if 'profit' in vars:
        df = df[df['profit'] != 'FALSE']
        df['profit'] = df['profit'].astype(int)
    df.dropna(inplace=True)
    df = df.to_numpy()
    return df

def elbow_point_plot(cluster, errors):
    """
    This function helps create a plot representing the tradeoff between the
    number of clusters and the inertia values.

    :param cluster: 1D np array that represents K (the number of clusters)
    :param errors: 1D np array that represents the inertia values
    """
    plt.clf()
    plt.plot(cluster, errors)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('elbow_plot')
    plt.show()

def find_K(data):
    Ks = [0] * MAX_K
    inertias = [None] * MAX_K
    for i in range(MAX_K):
        K = i + 1
        Ks[i] = K
        km = Kmeans(data, K, 100)
        centroids, indices = km.run()
        inertias[i] = km.inertia(centroids, indices)
    elbow_point_plot(Ks, inertias)

def get_min_max(data):
    mins = np.min(data, axis=0, keepdims =True)
    maxes = np.max(data, axis=0, keepdims =True)
    return mins, maxes

def min_max_scale(data):
    new_data = (data - np.min(data, axis=0, keepdims=True)) \
        / (np.max(data, axis=0, keepdims=True) - np.min(data, axis=0, keepdims=True))
    return new_data

def pct_top_votes(row):
    sum = float(row['votes_10'] + row['votes_9'] + row['votes_8'])
    total = float(row['total_votes'])
    return (sum/total)

def add_pct_8_10_votes(file_path):
    df = pd.read_csv(file_path)
    df['pct_8_10_votes'] = df.apply(lambda row: pct_top_votes(row), axis=1)
    return df

def whole_thing(file_path, vars):
    data = None
    if 'mean_vote' in vars:
        print('MEAN VOTE:')
        data = get_data(file_path, vars)
    elif 'profit' in vars:
        print('PROFIT:')
        data = get_data(file_path, vars)
    else:
        print('PERCENTAGE OF 8, 9, AND 10 VOTES:')
        df = add_pct_8_10_votes(file_path)
        df['series'] = (df['series'] == 'YES').astype(int)
        df = df[vars]
        data = df.to_numpy()
    mins, maxes = get_min_max(data)
    print('mins: ', mins)
    print('maxes: ', maxes)
    data = min_max_scale(data)

#     find_K(data)

    K = 4
#     if 'pct_8_10_votes' in vars:
#         K = 3
    km = Kmeans(data, K, MAX_ITER)
    centroids, indices = km.run()
    inertia = km.inertia(centroids, indices)

    print('min max centroids:')
    print(centroids)
    print('inertia: ', inertia)

    adjusted_centroids = []
    for centroid in centroids:
        new_centroid = [0] * len(centroid)
        for i in range(len(centroid)):
            new_centroid[i] = centroid[i] * (maxes[0][i] - mins[0][i]) + mins[0][i]
        adjusted_centroids.append(new_centroid)
    adjusted_centroids = np.array(adjusted_centroids)

    print('adjusted centroids: ', vars)
    print(adjusted_centroids)

def summ_stats(file_path, var):
    print('SUMMARY STATISTICS FOR ', var)
    df = pd.read_csv(file_path)[var]
    info = df.to_numpy()
    print('min: ', np.min(info))
    print('25th percentile: ', np.quantile(info, .25))
    print('median: ', np.quantile(info, .5))
    print('75th percentile: ', np.quantile(info, .75))
    print('max: ', np.max(info))
    print('mean: ', np.mean(info))
    print('standard deviation: ', np.std(info))
    print('variance: ', np.var(info))

def pct_summ_stats(file_path):
    print('SUMMARY STATISTICS FOR pct_8_10_votes')
    df = pd.read_csv(file_path)[['votes_10', 'votes_9', 'votes_8', 'total_votes']]
    df['pct_8_10_votes'] = df.apply(lambda row: pct_top_votes(row), axis=1)
    print(df)
    del df['votes_10']
    del df['votes_9']
    del df['votes_8']
    del df['total_votes']
    print(df)
    info = df.to_numpy()
    print('min: ', np.min(info))
    print('25th percentile: ', np.quantile(info, .25))
    print('median: ', np.quantile(info, .5))
    print('75th percentile: ', np.quantile(info, .75))
    print('max: ', np.max(info))
    print('mean: ', np.mean(info))
    print('standard deviation: ', np.std(info))
    print('variance: ', np.var(info))

class Kmeans:
    def __init__(self, X, K, max_iters):
        # Data
        self.X = X
        # Number of clusters
        self.K = K
        # Number of maximum iterations
        self.max_iters = max_iters
        # Initialize centroids
        self.centroids = self.init_centroids()

    def init_centroids(self):
        unique_rows = np.unique(self.X, axis=0)
        centroids = random.sample(unique_rows.tolist(), self.K)
        return np.array(centroids)

    def euclidean_dist(self, x, y):
        return np.linalg.norm(x - y)

    def closest_centroids(self):
        closest_centroids = []
        for x in self.X:
            min_dist = float('inf')
            min_dist_centroid = 0
            for i in range(len(self.centroids)):
                centroid = self.centroids[i]
                dist = self.euclidean_dist(x, self.centroids[i])
                if dist < min_dist:
                    min_dist = dist
                    min_dist_centroid = i
            closest_centroids.append(min_dist_centroid)
        return np.array(closest_centroids)

    def compute_centroids(self, centroid_indices):
        clusters = [None] * len(self.centroids)
        for i in range(len(clusters)):
            clusters[i] = []
        # sort data points by centroid
        for i in range(len(centroid_indices)):
            centroid_index = centroid_indices[i]
            clusters[centroid_index].append(self.X[i])
        convergence = True
        new_centroids = [None] * len(self.centroids)
        it = 0
        while it < self.K:
            # compute the average for centroid i
            new_centroids[it] = np.mean(np.array(clusters[it]), axis=0)
            # check if the average is different from the current centroid location
            if not np.array_equal(new_centroids[it], self.centroids[it]):
                convergence = False
                break
            it = it + 1
        for i in range((it + 1), self.K):
            new_centroids[i] = np.mean(np.array(clusters[i]), axis=0)
        self.centroids = new_centroids
        return convergence

    def run(self):
        it = 0
        convergence = False
        while (not convergence) and it < self.max_iters:
            closest_centroids = self.closest_centroids()
            convergence = self.compute_centroids(closest_centroids)
            it = it + 1
        indices = self.closest_centroids()
        return (np.array(self.centroids), np.array(indices))

    def inertia(self, centroids, centroid_indices):
        inertia = 0.0
        for i in range(len(centroid_indices)):
            x = self.X[i]
            centroid = centroids[centroid_indices[i]]
            dist = self.euclidean_dist(x, centroid)
            dist = dist ** 2
            inertia = inertia + dist
        return inertia

if __name__ == '__main__':
    file_path = 'Data/all_movies_table.csv'

#     summ_stats(file_path, 'mean_vote')
#     pct_summ_stats(file_path)


    vars1 = ['popular_actors', 'series', 'mean_vote']
    # originally: month, popular_actors, series
    whole_thing(file_path, vars1)

    print('--------------------------------------------------------------')

    vars2 = ['popular_actors', 'series', 'profit']
    # originally: month, popular_actors, series
    whole_thing(file_path, vars2)

    print('--------------------------------------------------------------')

    vars3 = ['popular_actors', 'series', 'pct_8_10_votes']
    whole_thing(file_path, vars3)


""" some results:
MEAN VOTE:
mins:  [[0.  0.  1.3]]
maxes:  [[15.   1.   9.3]]
min max centroids:
[[0.58786829 0.         0.66006877]
 [0.25031226 1.         0.59941452]
 [0.17522964 0.         0.62721121]
 [0.64876435 1.         0.67163602]]
inertia:  1153.0669152267567
adjusted centroids:  ['popular_actors', 'series', 'mean_vote']
[[8.81802438 0.         6.58055019]
 [3.75468384 1.         6.09531616]
 [2.62844456 0.         6.3176897 ]
 [9.73146527 1.         6.67308815]]
--------------------------------------------------------------
PROFIT:
mins:  [[         0          0 -165710090]]
maxes:  [[        15          1 2550965087]]
min max centroids:
[[0.2729386  0.         0.0697689 ]
 [0.53243311 0.         0.07480036]
 [0.76256324 0.         0.07636998]
 [0.52716763 1.         0.11621534]]
inertia:  105.81908264087012
adjusted centroids:  ['popular_actors', 'series', 'profit']
[[4.09407895e+00 0.00000000e+00 2.38293459e+07]
 [7.98649662e+00 0.00000000e+00 3.74982016e+07]
 [1.14384486e+01 0.00000000e+00 4.17623291e+07]
 [7.90751445e+00 1.00000000e+00 1.50009248e+08]]

Interpretations
Mean Vote:
 - on average, more popular actors means higher mean vote
Profit
 - movies with more popular actors have more profit
 - if it has many popular actors AND it's in a series, it has significantly more
 profit than if it has many popular actors and it is not in a series (second and fourth
 rows)


MEAN VOTE:
mins:  [[0.  0.  1.3]]
maxes:  [[15.   1.   9.3]]
min max centroids:
[[0.62898974 0.         0.66099294]
 [0.20887655 0.         0.63149778]
 [0.24929412 1.         0.59970588]
 [0.64791788 1.         0.67101249]]
inertia:  1154.7238358431202
adjusted centroids:  ['popular_actors', 'series', 'mean_vote']
[[9.43484615 0.         6.58794349]
 [3.13314825 0.         6.35198223]
 [3.73941176 1.         6.09764706]
 [9.71876816 1.         6.66809994]]
--------------------------------------------------------------
PROFIT:
mins:  [[         0          0 -165710090]]
maxes:  [[        15          1 2550965087]]
min max centroids:
[[0.27318888 0.         0.07019603]
 [0.64107048 0.         0.0752877 ]
 [0.68576942 1.         0.13454829]
 [0.31641026 1.         0.09185368]]
inertia:  97.91936012869158
adjusted centroids:  ['popular_actors', 'series', 'profit']
[[4.09783322e+00 0.00000000e+00 2.49897314e+07]
 [9.61605723e+00 0.00000000e+00 3.88221263e+07]
 [1.02865412e+01 1.00000000e+00 1.99813913e+08]
 [4.74615385e+00 1.00000000e+00 8.38265111e+07]]

Interpretations
Mean Vote: -- same as above
Profit: -- same as above
 - comparing first and last rows --> greater profit for the one that's in a series
 - comparing second and third rows --> greater profit for the one that's in a series

"""