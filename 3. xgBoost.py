import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import r2_score

with open("기말과제/modeling/xList.pkl", 'rb') as f:
    xList = np.array(pickle.load(f))
with open("기말과제/modeling/yList.pkl", 'rb') as f:
    yList = np.array(pickle.load(f))

from sklearn.model_selection import train_test_split
train_input, test_input, train_target, test_target = train_test_split(
    xList, yList, random_state = 42, test_size = 0.2
)

train_target_lat = train_target[:,0]
train_target_lon = train_target[:,1]
test_target_lat = test_target[:,0]
test_target_lon = test_target[:,1]

from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree = 5, include_bias = False)
poly.fit(train_input)
train_poly = poly.transform(train_input)
test_poly = poly.transform(test_input)

with open("기말과제/modeling/finalModel/xgboost_poly_model.pkl", 'wb') as f:
    pickle.dump(poly, f)

from xgboost import XGBRegressor

xgb_lat = XGBRegressor(random_state = 42, max_depth = 3, min_child_weight = 1, n_estimators = 100)
xgb_lon = XGBRegressor(random_state = 42, max_depth = 3, min_child_weight = 1, n_estimators = 100)
xgb_lat.fit(train_poly, train_target_lat)
xgb_lon.fit(train_poly, train_target_lon)

prediction_lat = xgb_lat.predict(test_poly)
prediction_lon = xgb_lon.predict(test_poly)

print("훈련세트 점수 (위도) : ", xgb_lat.score(train_poly, train_target_lat))
print("훈련세트 점수 (경도) : ", xgb_lon.score(train_poly, train_target_lon))
print("테스트세트 점수 (위도) : ", r2_score(test_target_lat, prediction_lat))
print("테스트세트 점수 (경도) : ", r2_score(test_target_lon, prediction_lon))

with open('기말과제/modeling/finalModel/xgboost_lat.pkl', 'wb') as file:
    pickle.dump(xgb_lat, file)
with open('기말과제/modeling/finalModel/xgboost_lon.pkl', 'wb') as file:
    pickle.dump(xgb_lon, file)