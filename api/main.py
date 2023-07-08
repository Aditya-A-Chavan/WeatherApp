from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def weather():
    api_key = 'c70f6f3bf64ab7edc365a23b47a6f5d6'
    if request.method == 'POST':
        location = request.form['location']
        layer = request.form.get('layer', 'clouds_new')  # Use 'clouds_new' as default if layer is not specified
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        url_geocoder = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=2&appid={api_key}'
        response1 = requests.get(url_geocoder)
        data1 = response1.json()
        city_id = data['id']
        if response.status_code == 200:
            weather_data = {
                'location': data['name'],
                'temperature': round(data['main']['temp']),
                'condition': data['weather'][0]['description'],
                'FeelsLike': round(data['main']['feels_like']),
                'MaxTemp': round(data['main']['temp_max']),
                'MinTemp': round(data['main']['temp_min'])
            }
            latitude =[
                'lat': data1[0]['lat'],
                'long': data1[0]['lon']
            }
            latitude_aqi = latitude.get('lat')
            longitude_aqi = latitude.get('long')
            return render_template('weather.html', weather=weather_data, latitude=latitude, api_key=api_key, layer=layer, city_id=city_id)
        else:
            error_message = data['message']
            return render_template('weather.html', error=error_message)
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)
