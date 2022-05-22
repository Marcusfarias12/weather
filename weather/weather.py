import requests
import datetime 
from datetime import date, datetime
import time 
import matplotlib.pyplot as plt
import csv
import json
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from validators import length
import numpy as np
import seaborn as sns
import pandas as pd

sns.set_style('darkgrid')
from matplotlib.pyplot import figure
figure(figsize=(8, 6))

today = date.today()
now = datetime.now().time()
current_time = now.strftime("%H_%M_%S")
current_day = today.strftime("%d_%m ")
time_now = current_day + current_time

lat,lon = 
API_key = ''

def city_forecast(lat, lon):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts,daily&appid=')
    return response.json()

with open('weather\weather_info.json', 'w', encoding='utf-8') as f:
    json.dump(city_forecast(lat,lon), f, ensure_ascii=False, indent=4)

f = open('weather\weather_info.json')
data = json.load(f)


"""
data = pd.DataFrame(data = data['hourly'])
d = {'date':data['dt'], "rain": data['rain']}
df = pd.DataFrame(data = d).dropna()
df_rain = df['rain'].apply(pd.Series)
df = df.drop(columns=['rain'])

df = pd.concat([df, df_rain], axis=1)
print(df)"""


data_hour = data['hourly']


hum_now = data_hour[0]['humidity']
clouds_now = data_hour[0]['clouds']
weather_now = data_hour[0]['weather'][0]['main']
description_now  = data_hour[0]['weather'][0]['description']


x = []
y = []
z = []
d = []

for i in range(0, len(data_hour)):
    ts = data_hour[i]['dt']
    date = datetime.utcfromtimestamp(ts).strftime('%d-%m %H:%M') #'%d-%m %H:%M' #%d\n%H
    x.append(date)
    tem = data_hour[i]['temp'] 
    prob = data_hour[i]['pop']
    description  = data_hour[i]['weather'][0]['description']
    y.append(tem - 273.15)
    d.append(description)
    z.append(prob)
    
"""sns.histplot(y, color = 'g')
sns.kdeplot(y)
sns.distplot(y)
plt.xlim(0,1)"""

"""plt.scatter(x,y, c = 'orange')
plt.plot(x,y, '--',c = 'r')

plt.scatter(x, z, c = 'g')
plt.plot(x, z)"""

"""fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(x, y, 'orange')
ax2.plot(x, z, 'b-')

ax1.scatter(x, y, c = 'r')
ax2.scatter(x, z, c = 'g')

ax1.set_ylabel('Temperature', color='orange')
ax2.set_ylabel('Probability of rain', color='b')"""


data = {'dates': x, 'temp' : y, 'description': d}
data = pd.DataFrame(data)
#print(data)
palette = sns.color_palette("hls", len(set(data['description'])))


plt.title(f"Temperature at lat = {lat}, lon = {lon}", fontsize = 14)
plt.ylabel("Temperature [ºC]")
plt.xticks(rotation=70)
plt.plot(x, y, '--', c = 'g', linewidth=2, label = f'The humidity now is {hum_now}% \nThe clouds now are {clouds_now}% \nThe weather now is {weather_now}, description is {description_now}')
sns.scatterplot(data=data, x="dates", y="temp", hue="description",s = 100, palette=palette)
#plt.scatter(x,y, color = 'c', s = 100)
plt.xticks(x[::4] + [x[-1]])
plt.xlim(x[0], x[-1])
plt.legend()
plt.show()
    
