import os, math, json, datetime

def getCourse(lat1, lat2, lon1, lon2, weight = 0):
    lat1, lat2, lon1, lon2 = map(math.radians, [lat1, lat2, lon1, lon2])
    
    diff_lon = lon2 - lon1
    
    x = math.sin(diff_lon) * math.cos(lat2)
    y = (math.cos(lat1) * math.sin(lat2)) - (math.sin(lat1) * math.cos(lat2) * math.cos(diff_lon))
    course = math.atan2(x, y)

    course = math.degrees(course)
    
    course = (course + 360 + weight) % 360
    return course

def getDistance(lat1, lat2, lon1, lon2):
    lat1, lat2, lon1, lon2 = map(math.radians, [lat1, lat2, lon1, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    
    distance = R * c
    return distance

def getLoc(fileLoc):
    with open(fileLoc, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    predictList = []
    dataInfo = []

    for i in range(len(json_positions) - 1, 0, -1):
        thisTime = datetime.datetime.strptime(json_positions[i]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
        nextTime = datetime.datetime.strptime(json_positions[i-1]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
        diffTime = int((nextTime - thisTime).seconds / 60)
        distance = getDistance(json_positions[i]["lat"], json_positions[i-1]["lat"], json_positions[i]["lon"], json_positions[i-1]["lon"])

        if(diffTime >= 2):
            if(json_positions[i]["speed"] >= 3):
                predict = [diffTime, [json_positions[i]["lat"], json_positions[i]["lon"]], [json_positions[i-1]["lat"], json_positions[i-1]["lon"]]]
                info = [i, json_positions[i]["speed"], json_positions[i]["course"], thisTime, nextTime]

                predictList.append(predict)
                dataInfo.append(info)
            else:
                predict = [diffTime, [json_positions[i]["lat"], json_positions[i]["lon"]], [json_positions[i-1]["lat"], json_positions[i-1]["lon"]]]
                info = [i, round(distance / 1.852 / diffTime, 1), getCourse(json_positions[i]["lat"], json_positions[i-1]["lat"], json_positions[i]["lon"], json_positions[i-1]["lon"]), thisTime, nextTime]

                predictList.append(predict)
                dataInfo.append(info)

    return predictList, dataInfo

def createRow(lat, lon, speed, course, time):
    row = {
        "lat" : lat,
        "lon" : lon,
        "speed" : speed,
        "course" : course,
        "heading" : 'null',
        "destination" : 'null',
        "last_position_epoch" : 'null',
        "last_position_UTC" : time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    return row

def inputRow(newRow, fileLoc, info, fileName):
    with open(fileLoc, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    with open("기말과제/predictData/Data_time_원본/" + fileName, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)

    for i in range(len(info)):
        for k in range(len(newRow[i])):
            json_positions.insert(info[i][0], newRow[i][k])

    print(fileLoc)
    with open(fileLoc, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)

def main(predict, info):
    max_count = predict[0] - 1

    trans_lat, trans_lon = predict[1][0], predict[1][1]
    obj_lat, obj_lon = predict[2][0], predict[2][1]

    criDistance_lat = (obj_lat - trans_lat) / max_count
    criDistance_lon = (obj_lon - trans_lon) / max_count

    speed, course, time = info[1], info[2], info[3]
  
    result = []
    for i in range(max_count):
        trans_lat += criDistance_lat
        trans_lon += criDistance_lon
        time = time + datetime.timedelta(minutes = 1)

        if(getDistance(trans_lat, obj_lat, trans_lon, obj_lon) <= (speed / 60 * 1.852)):
            break

        result.append(createRow(trans_lat, trans_lon, speed, course, time))

    return result

yearList = ['2022', '2023', '2024']
monthList = ['04', '05', '09', '10', '11']

shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append(data[1])

for i in range(len(shipList)):
    shipName = str(shipList[i])
    for y in yearList:
        for m in monthList:
            for d in range(1, 30):
                df = ('0' + str(d)) if d < 10 else str(d)
                fileName = shipName + "_" + str(y) + "-" + str(m) + "-" + df
                fileLoc = "기말과제/Data/" + str(y) + "/" + shipName + "/" + str(m) + "월/"
                fileLoc += fileName + ".json"

                if(os.path.exists(fileLoc)):
                    predictList, dataInfo = getLoc(fileLoc)
                    if(len(predictList) > 0):
                        with open(fileLoc, encoding = 'utf-8') as json_file:
                            data = json.load(json_file)
                            json_positions = data["data"]["positions"]

                        newRow =  []
                        for k in range(len(predictList)):
                            result = main(predictList[k], dataInfo[k])
                            newRow.append(result)
                        
                        inputRow(newRow, fileLoc, dataInfo, fileName)