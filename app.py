from flask import Flask, render_template, request, jsonify
import pycountry
import requests

app = Flask(__name__)

# Define a function to get weather data using OpenWeatherMap API
def get_weather_data(city, unit):
    api_key = 'Your API key'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': unit}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Define a function to get temperature for a city using OpenWeatherMap API
def get_temperature(city):
    # Fetch temperature for the city using OpenWeatherMap API
    api_key = 'Your API key'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  # Use 'imperial' for Fahrenheit
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'main' in data and 'temp' in data['main']:
        return data['main']['temp']
    else:
        return 'N/A'

# Define a custom Jinja2 filter for zipping lists
def custom_zip(a, b):
    return zip(a, b)

app.jinja_env.filters['zip'] = custom_zip

@app.route('/', methods=['GET', 'POST'])
def index():
    countries = [{'code': country.alpha_2, 'name': country.name} for country in pycountry.countries]

    # Example cities (you can replace these with your desired cities)
    city_names = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai']
    city_temperatures = [get_temperature(city) for city in city_names]

    weather_data = None  # Default value

    if request.method == 'POST':
        city = request.form['city']
        unit = request.form['unit']
        weather_data = get_weather_data(city, unit)
        city_temperatures = [get_temperature(city) for city in city_names]  # Update temperatures

    return render_template('index.html', weather_data=weather_data, countries=countries,
                           city_names=city_names, city_temperatures=city_temperatures)


@app.route('/get_temperature/<city>', methods=['GET'])
def get_city_temperature(city):
    temperature = get_temperature(city)
    return jsonify({'temperature': temperature})

if __name__ == '__main__':
    app.run(debug=True)
