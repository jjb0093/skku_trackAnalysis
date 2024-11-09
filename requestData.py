shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append((data[0], data[1]))

dateList = [
    ['2024-04-29', '2024-05-03'],
    ['2024-05-18', '2024-05-24'],
    ['2024-06-16', '2024-06-21'],
    ['2024-08-28', '2024-09-01'],
    ['2024-10-07', '2024-10-13'],
    ['2024-11-01', '2024-11-08']
]

import requests
import json
import os

for i in range(20, len(shipList)):
    print(shipList[i][0])
    for k in range(len(dateList)):
        requestURL = "https://api.datalastic.com/api/v0/vessel_history?api-key=#&mmsi="
        requestURL += str(shipList[i][0])+"&from="+str(dateList[k][0])+"&to="+str(dateList[k][1])
        
        r = requests.get(url = requestURL)
        r_dict = json.loads(r.text)

        folder_path = "기말과제/Data/"+str(shipList[i][1])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = "기말과제/Data/"+str(shipList[i][1])+"/"+str(shipList[i][1])+"_"+str(k)+".json"
        with open(file_path, 'w') as f:
            json.dump(r_dict, f)