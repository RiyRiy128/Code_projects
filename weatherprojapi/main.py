import requests
from twilio.rest import Client

Open_weather_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "997cea8fbf68198c8760c0e65ecb2d20"
account_sid = "ACe433c606a7e0f2492bd7b87f8ceb5a3a"
auth_token = "1fe604850541959fecc571f8d4894933"


#Amz CPT14
weath_params = {
    "appid": api_key,
    "lat": 46.947975,
    "lon": 7.447447,
    "cnt": 4
}

#Get the weather details for location with HTTP request to Openweather API
resp = requests.get(Open_weather_endpoint, params=weath_params)

#Raise an exception if response is not 200
resp.raise_for_status()

#Extract the json from response
weather_data = resp.json()

#Check weather classification code
#print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]

    #By standards of the openweather weather codes, if anything is under 700 it should rain
    if int(condition_code) < 700:
        will_rain = True

#simulate response due to restrictions
if will_rain:
    print("Bring an umbrella")

else:
    print("You're safe, no umbrella needed")

#if true, send message to user via twilio API SMS. Would otherwise work but do to free account restrictions on twilio verified numbers
#if will_rain:
    #client = Client(account_sid, auth_token)
    #message = client.messages \
        #.create(
        #body="It's going to rain today. Remember to bring an ☔️",
        #from_="+13802079633",
        #to="+270742474308"
    #)
    #print(message.status)


#Again would otherwise work but do to the above, it is just a print statement

#else:
    #client = Client(account_sid, auth_token)
    #message = client.messages \
        #.create(
        #body="It's not going to rain today. Remember to bring an ☔️",
        #from_="+13802079633",
        #to="+27742474308"
    #)
    #print(message.status)
    