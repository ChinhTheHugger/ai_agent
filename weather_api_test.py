import requests

# OpenWeather
API_KEY = 'e1614efbfe8be4797e83cfadf361631f'
res = requests.get(f'https://api.openweathermap.org/data/4.0/onecall/current?lat=52.2297&lon=21.0122&units=metric&lang=en&appid={API_KEY}')

# # WeatherAPI
# API_KEY = '8c95e631d17446f0af4121245261007'
# res = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Tokyo')

print(res.json())