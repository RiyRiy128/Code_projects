# Weather API Project

A Python application that fetches weather data and sends SMS notifications based on weather conditions.

## Description

This project integrates with the OpenWeatherMap API to fetch weather forecasts and uses Twilio to send SMS notifications when rain is expected. It's designed to help users prepare for weather changes by receiving timely alerts.

## Features

- Weather data fetching from OpenWeatherMap API
- Rain prediction analysis
- SMS notification system via Twilio
- Location-based weather monitoring
- Automated weather condition checking

## Setup Requirements

1. **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api) to get your API key
2. **Twilio Account**: Create a Twilio account for SMS functionality
3. **Python Dependencies**: Run `pip install requests twilio`

## Configuration

Update the following in `main.py`:
- `api_key`: Your OpenWeatherMap API key
- `account_sid`: Your Twilio Account SID
- `auth_token`: Your Twilio Auth Token
- Coordinates (lat/lon) for your desired location

## How It Works

1. Fetches 4-hour weather forecast for specified coordinates
2. Analyzes weather condition codes to predict rain
3. Sends SMS notification if rain is expected
4. Provides console feedback about weather conditions

## Weather Conditions

- Weather codes below 700 indicate precipitation (rain/snow)
- The app checks multiple forecast periods for accuracy
- Sends appropriate messages based on weather predictions

## Dependencies Used

- Python
- OpenWeatherMap API
- Twilio SMS API
- HTTP requests handling
- JSON data processing

## Note

The SMS functionality is currently commented out due to Twilio account restrictions, but the weather checking logic is fully functional.