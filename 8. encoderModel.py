import pandas as pd
import numpy as np
import json, pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv("기말과제/encoding/result.csv").fillna(0)

scaler = StandardScaler()
data = scaler.fit_transform(df)

inputDim = data.shape[1]
batch_size = 128
epochs = 15

train_data, test_data = train_test_split(data, test_size = 0.2, random_state = 42)

encoder = Sequential()
encoder.add(Input(shape = (inputDim, )))
encoder.add(Dense(22, activation = 'relu'))
encoder.add(Dense(15, activation = 'relu'))

decoder = Sequential()
decoder.add(Input(shape = (15, )))
decoder.add(Dense(22, activation = 'relu'))
decoder.add(Dense(inputDim, activation = 'linear'))

autoencoder = Sequential([encoder, decoder])
autoencoder.compile(optimizer='adam', loss='mse')

history = autoencoder.fit(
    train_data, train_data,
    epochs = epochs,
    batch_size = batch_size,
    validation_data = (test_data, test_data),
    verbose = 2
)

all_decoded = autoencoder.predict(data)
all_errors = np.mean((scaler.inverse_transform(data) - scaler.inverse_transform(all_decoded)) ** 2, axis=1)

threshold = np.percentile(all_errors, 95)

with open("기말과제/outlierDectection/scaler.pkl", 'wb') as f:
    pickle.dump(scaler, f)
with open("기말과제/outlierDectection/encoder.pkl", 'wb') as f:
    pickle.dump(encoder, f)
with open("기말과제/outlierDectection/decoder.pkl", 'wb') as f:
    pickle.dump(decoder, f)
with open("기말과제/outlierDectection/encoderThreshold.pkl", 'wb') as f:
    pickle.dump(threshold, f)
