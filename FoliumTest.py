import decimal
import folium

import json
file = "기말과제/hangang.json"
with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)

json_position = data["data"]["positions"]

loc = []
for i in range(len(json_position)):
    lis = [json_position[i]["lat"], json_position[i]["lon"]]
    loc.append(lis)

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

        #print(loc_data)

folium.Marker([37.670, 125.640], popup='<b>START</b>').add_to(myMap)
folium.Marker([37.070, 126.640], popup='<b>FINISH</b>').add_to(myMap)

for i in range(len(json_position)):
    folium.Marker([json_position[i]["lat"], json_position[i]["lon"]], popup='<b>'+str(i)+'</b>').add_to(myMap)

folium.PolyLine(locations=loc, color='red').add_to(myMap)

myMap.save('index.html')