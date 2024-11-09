import json

shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append((data[0], data[1]))

countList = []
for i in range(len(shipList)):
    for k in range(6):
        shipName = shipList[i][1]
        file = "기말과제/Data/"+str(shipName)+"/"+str(shipName)+"_"+str(k)+".json"
        print(file)
        with open(file, encoding='utf-8') as json_file:
            data = json.load(json_file)
            json_positions = data["data"]["positions"]

        print(str(shipName)+"_"+str(k)+".json -> " + str(len(json_positions)))
        countList.append(len(json_positions))
print("총 합계 : ", sum(countList))
print("평균 수 : ", sum(countList) / (len(shipList) * 6))