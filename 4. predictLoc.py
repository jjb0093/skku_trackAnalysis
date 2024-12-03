import pickle, json, datetime, math, os

with open("기말과제/modeling/finalModel/xgboost_lat.pkl", 'rb') as f:
    model_lat = pickle.load(f)
with open("기말과제/modeling/finalModel/xgboost_lon.pkl", 'rb') as f:
    model_lon = pickle.load(f)
with open("기말과제/modeling/finalModel/xgboost_poly_model.pkl", 'rb') as f:
    poly = pickle.load(f)

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
    if os.path.exists(fileLoc):
        with open(fileLoc, encoding='utf-8') as json_file:
            data = json.load(json_file)
            json_positions = data["data"]["positions"]

        predictList = []
        dataInfo = []

        for i in range(len(json_positions) - 1, 0, -1):
            thisTime = datetime.datetime.strptime(json_positions[i]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
            nextTime = datetime.datetime.strptime(json_positions[i-1]["last_position_UTC"], '%Y-%m-%dT%H:%M:%SZ')
            diffTime = int((nextTime - thisTime).seconds / 60)

            distance = getDistance(json_positions[i]["lat"], json_positions[i-1]["lat"], json_positions[i]["lon"], json_positions[i-1]["lon"])

            if((diffTime >= 40) and (diffTime <= 300) and (distance >= 10)):
                calCourse = getCourse(json_positions[i]["lat"], json_positions[i-1]["lat"], json_positions[i]["lon"], json_positions[i-1]["lon"], -5)
                meanCourse = (calCourse * 3 + json_positions[i]["course"] * 2) / 5

                xListForPredict = [json_positions[i]["speed"], meanCourse, diffTime]
                info = [i, thisTime, [json_positions[i]["lat"], json_positions[i]["lon"]], [json_positions[i-1]["lat"], json_positions[i-1]["lon"]]]

                predictList.append(xListForPredict)
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

def inputRow(newRow, fileLoc, fileName, count, year):
    with open(fileLoc, encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    for i in range(len(count)):
        for k in range(len(newRow[i])):
            json_positions.insert(count[i], newRow[i][k])
    
    with open(fileLoc, "w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4)
    
def predict(xList):
    x_poly = poly.transform([xList])

    result_lat = model_lat.predict(x_poly)[0]
    result_lon = model_lon.predict(x_poly)[0]

    return [result_lat, result_lon]

def main(xList, info, criTime = 10):
    newLoc = []
    newRow_list = []
    newRow = []

    diffTime = xList[2]
    xList[0] = 8 if xList[0] < 8 else xList[0]
    xList[2] = criTime

    trans_time = info[1]
    trans_lat = info[2][0]
    trans_lon = info[2][1]

    obj_lat = info[3][0]
    obj_lon = info[3][1]

    minDistance = round(xList[0] * criTime / 60 * 1.852, 2)

    newLoc.append([trans_lat, trans_lon])

    count = 0
    while(getDistance(trans_lat, obj_lat, trans_lon, obj_lon) >= minDistance):
        result = predict(xList)
        count += 1

        trans_lat += result[0]
        trans_lon += result[1]

        new_course = getCourse(trans_lat, obj_lat, trans_lon, obj_lon)

        xList[1] = new_course
        newLoc.append([trans_lat, trans_lon])
        newRow_list.append([trans_lat, trans_lon, xList[0], new_course, None])
    
    timeGap = int(diffTime / count)
    newRow_list[0][4] = trans_time + datetime.timedelta(minutes = timeGap)
    for l in range(1, len(newRow_list)):
        newRow_list[l][4] = newRow_list[l-1][4] + datetime.timedelta(minutes = timeGap)
    for l in range(len(newRow_list)):
        newRow.append(createRow(*newRow_list[l]))

    newLoc.append([obj_lat, obj_lon])

    return newLoc, newRow


colors = ['blue', 'yellow', 'green', 'purple', 'orange']

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

                imageLoc = "기말과제/Image/" + str(y) + "/" + shipName + "/"
                imageLoc += fileName + ".png"

                if(os.path.exists(fileLoc)):
                    predictList, dataInfo = getLoc(fileLoc)
                    if(len(predictList) > 0):

                        with open(fileLoc, encoding='utf-8') as json_file:
                            data = json.load(json_file)
                            json_positions = data["data"]["positions"]

                        loc = []
                        for p in range(len(json_positions)-1, 0, -1):
                            lis = [json_positions[p-1]["lat"], json_positions[p-1]["lon"]]
                            loc.append(lis)
                        
                        newRow, count = [], []
                        for k in range(len(predictList)):
                            newLoc, rows = main(predictList[k], dataInfo[k])
                            newRow.append(rows)
                            count.append(dataInfo[k][0])
                        
                        inputRow(newRow, fileLoc, fileName, count, y)
                
                else: print()