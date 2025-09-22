import requests

from twilio.rest import Client

weather_api_url = "https://api.openweathermap.org/data/2.5/forecast"
weather_key = "997cea8fbf68198c8760c0e65ecb2d20"
twilio_account = "ACe433c606a7e0f2492bd7b87f8ceb5a3a"
twilio_token = "1fe604850541959fecc571f8d4894933"


#Amz CPT14
request_params = {
    "appid": weather_key,
    "lon": 18.46,
    "lat": 33.94,
    "cnt": 4
}

# Fetch weather forecast data
api_response = requests.get(weather_api_url, params=request_params)


api_response.raise_for_status()

# Parse JSON response
forecast_data = api_response.json()

#Check weather classification code
#print(forecast_data["list"][0]["weather"][0]["id"])

rain_expected = False

# Check each forecast period
for forecast_period in forecast_data["list"]:
    weather_id = forecast_period["weather"][0]["id"]
    
    #By standards of the openweather weather codes, if anything is under 700 it should rain
    if weather_id < 700:
        rain_expected = True
        break

#simulate response due to restrictions
print("Bring an umbrella" if rain_expected else "You're safe, no umbrella needed")

#if true, send message to user via twilio API SMS. Would otherwise work but do to free account restrictions on twilio verified numbers
#if rain_expected:
    #sms_client = Client(twilio_account, twilio_token)
    #sms_message = sms_client.messages \
        #.create(
        #body="It's going to rain today. Remember to bring an ☔️",
        #from_="+13802079633",
        #to="+270742474308"
    #)
    #print(sms_message.status)


#Again would otherwise work but do to the above, it is just a print statement

#else:
    #sms_client = Client(twilio_account, twilio_token)
    #sms_message = sms_client.messages \
        #.create(
        #body="It's not going to rain today.",
        #from_="+13802079633",
        #to="+27742474308"
    #)
    #print(sms_message.status)
    