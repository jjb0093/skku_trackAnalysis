import json, os, datetime, math
import pandas as pd

def getDistance(lat1, lat2, lon1, lon2):
    lat1, lat2, lon1, lon2 = map(math.radians, [lat1, lat2, lon1, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # 하버사인 공식
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # 지구 반지름 (km)
    
    # 두 점 사이의 거리 계산
    distance = R * c
    return distance

def windowData(data, size):
    result_window = []
    count = 0

    window = []
    for i in range(len(data)):
        window += data[i]
        count += 1

        if(count == size):
            result_window.append(window)
            window = []
            count = 0

    return result_window

def createData(file_path, window):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    data = []
    for i in range(len(json_positions) - 2, -1, -1):
        lat = json_positions[i]["lat"]
        lon = json_positions[i]["lon"]
        speed = json_positions[i]["speed"]
        course = json_positions[i]["course"]

        diff_lat = round(json_positions[i]["lat"] - json_positions[i+1]["lat"], 6)
        diff_lon = round(json_positions[i]["lon"] - json_positions[i+1]["lon"], 6)

        thisTime = datetime.datetime.strptime(json_positions[i]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
        nextTime = datetime.datetime.strptime(json_positions[i-1]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')

        data.append([lat, lon, speed, course, diff_lat, diff_lon])

    data = windowData(data, window)
    return data

shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append((data[0], data[1]))

year = ["2022", "2023", "2024"]
monthList = ['04', '05', '09', '10', '11']

result = []
data = []

windows = 5

for y in year:
    for i in range(len(shipList)):
        shipName = shipList[i][1]
        for m in monthList:
            folder_path = "기말과제/Data/" + str(y) + "/" + str(shipName) + "/" + str(m) + "월"
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                for k in range(len(files)):
                    file_path = folder_path + "/" + files[k]
                    print(files[k])

                    data = createData(file_path, windows)
                    result += data

length = int(len(result[0]) / windows)
finalIndex = length * (windows - 1)
middleIndex = length * int((windows - 1) / 2)

removeList = []
for i in range(len(result)-1, -1, -1):
    if(result[i][2] <= 4 
       or result[i][0] < 37.1 or result[i][finalIndex] < 37.1
       or result[i][1] <= 125.96 or result[i][finalIndex+1] <= 125.96): 
        del result[i]

portIndex = []
for i in range(len(result)-1, -1, -1):
    if((getDistance(result[i][0], 37.4607, result[i][1], 126.5991) <= 10) or (getDistance(result[i][finalIndex], 37.4607, result[i][finalIndex+1], 126.5991) <= 10)):
        portIndex.append(i)
for i in range(len(portIndex)):
    if(i % 10 != 0): del result[portIndex[i]]

criLon, criLat = [37.3296, 37.3833], [126.2687, 126.5079]

portIndex = []
for i in range(len(result)-1, -1, -1):
    if(((result[i][middleIndex] >= criLon[0]) and (result[i][middleIndex] <= criLon[1]) and (result[i][middleIndex+1] >= criLat[0]) and (result[i][middleIndex+1] <= criLat[1]))):
       portIndex.append(i)
for i in range(len(portIndex)):
    if(i % 5 != 0): del result[portIndex[i]]

result_window = pd.DataFrame(result)
result_window.to_csv('기말과제/encoding/result.csv', index = False)