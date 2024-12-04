import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import norm

centroid_df = pd.read_csv("기말과제/encoding/centroid.csv")
vectors_df = pd.read_csv("기말과제/encoding/result.csv")

with open("기말과제/outlierDetection/scaler.pkl", 'rb') as f:
    scaler = pickle.load(f)

centroids = centroid_df.to_numpy()
input_vectors = vectors_df.to_numpy()

def cal_distances(vector, centroids):
    return euclidean_distances(vector, centroids)

mean_std_list = []
for centroid in centroids:
    distances = cal_distances(input_vectors, centroid.reshape(1, -1)).flatten()
    mean_std_list.append((np.mean(distances), np.std(distances)))

threshold5_list = []
threshold95_list = []
for mean_distance, std_distance in mean_std_list:
  threshold_5 = norm.ppf(0.05, mean_distance, std_distance)
  threshold_95 = norm.ppf(0.95, mean_distance, std_distance)
  threshold5_list.append(threshold_5)
  threshold95_list.append(threshold_95)

with open('기말과제/outlierDetection/mean_std_list.pkl', 'wb') as f:
  pickle.dump(mean_std_list, f)
with open('기말과제/outlierDetection/norm_threshold5.pkl', 'wb') as f:
  pickle.dump(threshold5_list, f)
with open('기말과제/outlierDetection/norm_threshold95.pkl', 'wb') as f:
  pickle.dump(threshold95_list, f)