# bloomsky2wu.py
# Simple script that reads the data for a BloomSky station from the BloomSky API, then parses that
# data and uploads it to the WeatherUnderground Private Weather Station

# Requires
# 1. A Bloomsky API Key (you find that for your station at https://dashboard.bloomsky.com/user
#    then click on "Developers" on the lower left and your API Key should be shown (will look
#    like sN-vtc_XXXXXXXXXXXXXXXXXXXXd8qtg== (not a real key)
# 2. A Weather Underground Account and Private Weather Station configured, and the WU PWS ID and Key
#    See https://www.wunderground.com/member/devices.
#    Station ID looks like KUTPARKC238, and Key looks KhExz5qS (not a real key)
# 3. Configuration below to be updated within
# 4. A task scheduler / cron job to run this script every X minutes (I do 5 and use Windows Task Scheduler in the background 

# This script known to work on Python 3.10.x on Windows.
# Simply change the paramters below and then invoke as an arguement to the python interpereter.

import urllib.request
import json

#Configure these parameters
debug_output = False # Set to True if you wnat debug to standard output, else leave as False
bloomsky_api_key = 'sN-vtc_XXXXXXXXXXXXXXXXXXXXXXXXxk=' # Replace XXXX with your Bloomsky API key
own_a_storm = True #change to False if you only have a BloomSky Sky device and not the optional Storm device
WU_station_id = "XXXXXXXXXX" # Replace with your Weather Underground PWS ID
WU_station_key = "YYYYYYYYY" # Replace YYYYYYYYY with your Weather Underground PWS Station Key

#Other parameters which should be consistent
bloomsky_api_url = "http://api.bloomsky.com/api/skydata/"
WU_api_url = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"

#Open up a web request to BloomSky using the API key configured above to authorize to retireve current data
bloomsky_req = urllib.request.Request(bloomsky_api_url,headers={'Authorization':bloomsky_api_key})
response = urllib.request.urlopen(bloomsky_req)

#Parse the resulting JSON data object
bloomsky_jsondata = json.loads(response.read().decode('utf-8'))

if debug_output == True :
    print("JSON DATA RECIEVED")
    print(json.dumps(bloomsky_jsondata, indent=4))

#Put the Sky JSON blocks into an array and pull pout the data we want
sky_data = (bloomsky_jsondata[0]['Data'])
humidity_str = str(sky_data['Humidity'])
temp_str = str(sky_data['Temperature'])
pressure_str = str(sky_data['Pressure'])

#If there is a Storm device then get data from the Strom section of the JSON
if own_a_storm == True:
    storm_data = (bloomsky_jsondata[0]['Storm'])
    wind_sustained_str = str(storm_data['SustainedWindSpeed'])
    wind_gust_str = str(storm_data['WindGust'])
    wind_dir_str = str(storm_data['WindDirection'])
    uv_index_str = str(storm_data['UVIndex'])
    rain_daily_str = str(storm_data['RainDaily'])
    rain_rate_str = str(storm_data['RainRate'])

    #Convert Bloomsky N, S, E, W, NE, NW, SE, SW into 360 degree values
    if wind_dir_str == 'N':
        wind_dir_todegrees= "360"

    elif wind_dir_str == "NE":
        wind_dir_todegrees = "45"

    elif wind_dir_str == "NW":
        wind_dir_todegrees = "315"

    elif wind_dir_str == "S":
        wind_dir_todegrees = "180"

    elif wind_dir_str == "SE":
        wind_dir_todegrees = "135"

    elif wind_dir_str == "SW":
        wind_dir_todegrees = "225"

    elif wind_dir_str == "E":
        wind_dir_todegrees = "90"

    elif wind_dir_str == "W": 
        wind_dir_todegrees = "270"
    
    else: 
        wind_dir_todegrees = "0"


#Now from a connection with Weather Underground and upload the data

WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_key
date_str = "&dateutc=now"
action_str = "&action=updateraw"

if own_a_storm == True:
    WU_upload_str = (
        WU_api_url +
        WUcreds +
        date_str +
        "&tempf=" + temp_str +
        "&baromin=" + pressure_str +
        "&humidity=" + humidity_str +
        "&windspeedmph=" + wind_sustained_str +
        "&windgustmph=" + wind_gust_str +
        "&winddir=" + wind_dir_todegrees +
        "&UV" + uv_index_str +
        "&dailyrainin" + rain_daily_str +
       # "&rainin" + rain_rate_str +  commenting out as BloomSky does rate per 10 minutes and WU does 60 minutes....ugh
        action_str)
else:
    WU_upload_str = (
        WU_api_url +
        WUcreds +
        date_str +
        "&tempf=" + temp_str +
        "&baromin=" + pressure_str +
        "&humidity=" + humidity_str +
        action_str)


#Now from a connection with Weather Underground and upload the data
wu_req = urllib.request.Request(WU_upload_str)
response = urllib.request.urlopen(wu_req)

