import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

df = pd.read_csv("기말과제/encoding/result.csv")
df = df.fillna(0)

scalar = StandardScaler()
data = scalar.fit_transform(df)

with open("기말과제/encoding/scalar.pkl", 'wb') as f:
    pickle.dump(scalar, f)

from sklearn.cluster import KMeans

num_clusters = 300
km = KMeans(n_clusters = num_clusters, random_state = 42)
km.fit(data)

centers = pd.DataFrame(scalar.inverse_transform(km.cluster_centers_))
centers.to_csv("기말과제/encoding/centroid.csv", index = False)