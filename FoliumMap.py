import decimal
import folium
import json

def getLoc(shipName, dateNum):
    file = "기말과제/Data/"+str(shipName)+"/"+str(shipName)+"_"+str(dateNum)+".json"
    print(file)
    with open(file, encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_positions = data["data"]["positions"]

    loc = []
    for i in range(len(json_positions)):
        lis = [json_positions[i]["lat"], json_positions[i]["lon"]]
        loc.append(lis)

    return json_positions, loc

myMap = folium.Map(location=[37.400, 126.150], zoom_start=11)

gap = [0.04, 0.05]
start_loc = [37.670, 125.640]
for k in range(15):
    for i in range(20):
        loc_data = [
            [decimal.Decimal(start_loc[0]) + (-1 * k * decimal.Decimal(gap[0])), decimal.Decimal(start_loc[1]) + (i * decimal.Decimal(gap[1]))],
            [decimal.Decimal(start_loc[0] - gap[0]) + (-1 * k * decimal.Decimal(gap[0])), decimal.Decimal(start_loc[1] + gap[1]) + (i * decimal.Decimal(gap[1]))]
        ]
        number = (i + 1) + (k * 20)
        folium.Rectangle(bounds = loc_data, tooltip = 'Sector_' + str(number), opacity = '0.2').add_to(myMap)

#folium.Marker([37.670, 125.640], popup='<b>START</b>').add_to(myMap)
#folium.Marker([37.070, 126.640], popup='<b>FINISH</b>').add_to(myMap)

color = ['red', 'blue', 'white', 'green', 'yellow']

shipList = []
with open ("기말과제/Data/shipList.txt", 'r', encoding='utf8') as f:
    for line in f.readlines():
        data = line.rstrip('\n').split("/")
        shipList.append((data[0], data[1]))

for i in range(5):
    for k in range(6):
        shipName = shipList[i][1]
        json_positions, loc = getLoc(shipName, k)
        for json_position in json_positions:
            #folium.Marker([json_position["lat"], json_position["lon"]], popup='<b>'+str(shipName)+'_'+str(k)+'</b>').add_to(myMap)
            folium.PolyLine(locations=loc, color=color[i], opacity = 0.5).add_to(myMap)

myMap.save('index.html')