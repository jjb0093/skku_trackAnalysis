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
monthList = ['04', '05', '09', '10', '11']

import requests
import json
import os

for i in range(51, len(shipList)):
    shipName = shipList[i][1]
    print(i, shipName)
    for m in monthList:
        for d in range(1, 30):
            df = ('0' + str(d)) if d < 10 else str(d)
            de = ('0' + str(d + 1)) if (d + 1) < 10 else str(d + 1)
            dateFrom = "2024-" + m + "-" + df
            dateEnd = "2024-" + m + "-" + de

            requestURL = "https://api.datalastic.com/api/v0/vessel_history?api-key=6ae269cf-c9d8-4813-bd0b-6931a169f0a2&mmsi="
            requestURL += str(shipList[i][0])+"&from="+dateFrom+"&to="+dateEnd

            r = requests.get(url = requestURL)
            r_dict = json.loads(r.text)

            if(len(r_dict["data"]["positions"]) > 10):
                folder_path = "기말과제/Data/" + str(shipName) + "/" + str(m) + "월"
                if not os.path.exists(folder_path): os.makedirs(folder_path)

                file_path = folder_path + "/" + shipName + "_" + str(dateFrom) + ".json"
                with open(file_path, 'w') as f:
                    json.dump(r_dict, f)