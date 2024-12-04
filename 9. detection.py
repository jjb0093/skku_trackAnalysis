import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import json, pickle

with open("기말과제/outlierDetection/norm_threshold5.pkl", 'rb') as f:
    threshold_5 = pickle.load(f)
with open("기말과제/outlierDetection/norm_threshold95.pkl", 'rb') as f:
    threshold_95 = pickle.load(f)
with open("기말과제/outlierDetection/mean_std_list.pkl", 'rb') as f:
    mean_std_list = pickle.load(f)

with open("기말과제/outlierDetection/scaler.pkl", 'rb') as f:
    scaler = pickle.load(f)
with open("기말과제/outlierDetection/encoder.pkl", 'rb') as f:
    encoder = pickle.load(f)
with open("기말과제/outlierDetection/decoder.pkl", 'rb') as f:
    decoder = pickle.load(f)
with open("기말과제/outlierDetection/encoderThreshold.pkl", 'rb') as f:
    threshold = pickle.load(f)

centroid_df = pd.read_csv("기말과제/encoding/centroid.csv")
centroids = centroid_df.to_numpy()

def cal_distances(vector, centroids):
    return euclidean_distances(vector, centroids)

def anomaly_kMeans(target, centroids, mean_std_list):
    distances = cal_distances(target, centroids).flatten()
    closest_centroid_idx = np.argmin(distances)
    mean_distance, std_distance = mean_std_list[closest_centroid_idx]
    print(closest_centroid_idx)

    z_score = (np.mean(distances) - mean_distance) / std_distance
    threshold5, threshold95 = threshold_5[closest_centroid_idx], threshold_95[closest_centroid_idx]

    return z_score < threshold5 or z_score > threshold95

def anomaly_encoder(target, encoder, decoder, threshold, scaler):
    target = scaler.transform(target)
    encoded = encoder.predict(target)

    decoded = decoder.predict(encoded)
    decoded = scaler.inverse_transform(decoded)

    error = np.mean((scaler.inverse_transform(target) - decoded) ** 2, axis=1)

    is_outlier = error > threshold

    return is_outlier

def extract_vector(file_path):
    print(file_path)
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        positions = data["data"]["positions"]

    vectors = []
    for i in range(1, 6):
        lat, lon, speed, course = positions[i]["lat"], positions[i]["lon"], positions[i]["speed"], positions[i]["course"]
        diff_lat = round(positions[i + 1]["lat"] - lat, 6)
        diff_lon = round(positions[i + 1]["lon"] - lon, 6)
        vectors += [lat, lon, speed, course, diff_lat, diff_lon]

    return np.array(vectors).reshape(1, -1)

target = extract_vector("기말과제/Data/senario1.json")

is_anomaly_kMeans = anomaly_kMeans(target, centroids, mean_std_list)
is_anomaly_encoder = anomaly_encoder(target, encoder, decoder, threshold, scaler)

if(is_anomaly_kMeans or is_anomaly_encoder): print("TRUE")
else: print("FALSE")