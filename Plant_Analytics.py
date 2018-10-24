from urllib2 import Request, urlopen
import datetime
import pytz
import requests
from datetime import datetime
from pytz import timezone
import time

light = Request('blynkApikey')
uv = Request('blynkApikey')
soil = Request('blynkApikey')


headers = {
  'Content-Type': 'application/json'
}


#-----------------------------------------------------------------

api_address = "openWeatherApiKey"
city = raw_input("City Name :")

url = api_address + city

json_data = requests.get(url).json()
cloud_percent = json_data['clouds']['all']
humidity_percent = json_data['main']['humidity']


#-----------------------------------------Push Data

morning_message = """
 {
   "body": ""
 }
"""

cloud_message = """
 {
   "body": "It's cloudy today, no need to water me too much!"
 }
"""
report = """
  {
    "body": "Today's report on LCD" 
  }
  """

water = """
  {
    "body":"Please Water me!"
  }
  """

uv_message = """
{
    "body":"Too Much UV, I'm BURNING Here!"
  }
  """
  
request3 = Request('blynkApikey',
data=report, headers=headers)

request = Request('blynkApikey', data=morning_message, headers=headers)

request2 = Request('blynkApikey', data=cloud_message, headers=headers)

request4 = Request('blynkApikey', data=water, headers=headers)

request5 = Request('blynkApikey', data=uv_message, headers=headers)
#---------------------------------------------------------------
request6 = Request('blynkApikey')

'''
request8 = Request('blynkApikey')

request9 = Request('blynkApikey')
'''

#--------------------------------------------------------------
request7 = Request('blynkApikey')

#---------------------------------------------------------------
print(str(cloud_percent) + "% cloudy")
#print(humidity_percent)


morning_counter = 0
count = 0
light_counter = 0
uv_counter = 0
soil_counter = 0
water_me = 0
burning = 0
button_counter = 0
#-------------------------------------------------------------------

while(True):
  date_object = datetime.now(pytz.timezone("America/Los_Angeles"))
  current_time = date_object.strftime('%H:%M:%S')

  response_soil = urlopen(soil).read()
  response_soil = response_soil[2:-2]
  response_soil = float(response_soil)

  response_light = urlopen(light).read()
  response_light = response_light[2:-2]
  response_light = float(response_light)

  #response_body = urlopen(request6).read()
  response_uv = urlopen(uv).read()
  response_uv = response_uv[2:-2]
  response_uv = float(response_uv)

  response_button = urlopen(request7).read()
  response_button = response_button[2:-2]
  response_button = float(response_button)

  if current_time == "07:00:00" and morning_counter == 0:#morning report
    if cloud_percent > 50:
      response_body = urlopen(request2).read()
    morning_counter = 1
  
  if current_time != "17:22:00" and morning_counter == 1: #morning report
    morning_counter = 0


  if current_time != "17:22:00": #summing data from all sensors
    count += 1
    light_counter += response_light
    uv_counter += float(response_uv)
    soil_counter += float(response_soil)
    time.sleep(1)

  if response_button == 1: #getting average and reporting it
    average_light = light_counter / count
    #average_uv = uv_counter / count
    average_soil = soil_counter / count
    request8 = Request('apiKey'%average_soil)
    request9 = Request('apiKey'%average_light)
    response_body = urlopen(request9).read()
    response_body = urlopen(request8).read()
    time.sleep(1)
    if current_time == "00:00:00":
      count = 0
      light_counter = 0
      uv_counter = 0
      soil_counter = 0
      

  if response_soil < 500 and water_me == 0:
    response_body = urlopen(request4).read()
    water_me = 1

  if response_soil >= 500 and water_me == 1:
    water_me = 0

  #response_uv = 8
  if response_uv >= 8 and burning == 0:
    response_body = urlopen(request5).read()
    burning = 1

  if response_uv < 8 and burning == 1:
    burning = 0
