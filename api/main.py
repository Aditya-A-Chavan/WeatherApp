from flask import Flask, render_template, request
import requests
import json

print(json.__version__)
print(requests.__version__)

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    location = request.args.get('location')
    api_key = '2ef114a28a8c41aabc7173812232806'
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'

    response = requests.get(url)
    data = json.loads(response.text)

    weather_data = {
        'location': data['location']['name'],
        'temperature': data['current']['temp_c'],
        'condition': data['current']['condition']['text']
    }

    return weather_data

if __name__ == '__main__':
    app.run()
