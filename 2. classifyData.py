import json
import os
import datetime
import pickle

def classifyIntoList(file_path):
    xList = []
    yList = []

    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    for i in range(len(json_positions) - 1, 0, -1):
        thisTime = datetime.datetime.strptime(json_positions[i]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
        nextTime = datetime.datetime.strptime(json_positions[i-1]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
        diffTime = int((nextTime - thisTime).seconds / 60)
        if((diffTime <= 20) and diffTime != 0 and (json_positions[i]["speed"] >= 4) and (json_positions[i]["speed"] <= 25)):
            xListForAppend = [json_positions[i]["speed"], json_positions[i]["course"], diffTime]
            yListForAppend = [round(json_positions[i-1]["lat"] - json_positions[i]["lat"], 5), round(json_positions[i-1]["lon"] - json_positions[i]["lon"], 5)]
            xList.append(xListForAppend)
            yList.append(yListForAppend)

    return xList, yList

def storeData(xList, yList):
    with open("기말과제/modeling/xList.pkl", 'wb') as f:
        pickle.dump(xList, f)
    with open("기말과제/modeling/yList.pkl", 'wb') as f:
        pickle.dump(yList, f)

shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append((data[0], data[1]))

monthList = ['04', '05', '09', '10', '11']

xList, yList = [], []
timeList = []
year = ["2022", "2023", "2024"]

for y in year:
    for i in range(len(shipList)):
        shipName = shipList[i][1]
        print(shipName)
        for m in monthList:
            folder_path = "기말과제/Data/" + str(y) + "/" + str(shipName) + "/" + str(m) + "월"
            print(folder_path)
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                for k in range(len(files)):
                    file_path = folder_path + "/" + files[k]

                    xData, yData = classifyIntoList(file_path)
                    xList += xData
                    yList += yData
                    #if(len(tData) != 0): timeList += (file_path.split('/')[4][:-5], tData)

storeData(xList, yList)