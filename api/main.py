from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def current_weather():
    from datetime import date
    global api_key
    api_key = 'c70f6f3bf64ab7edc365a23b47a6f5d6'
    if request.method == 'POST':
        location = request.form['location']

        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        url_geocoder = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=2&appid={api_key}'
        response1 = requests.get(url_geocoder)
        data1 = response1.json()

        url_fc = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}'
        response_fc = requests.get(url_fc)
        data_fc = response_fc.json()

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

            latitude = {
                'lat': data1[0]['lat'],
                'long': data1[0]['lon']
            }

            fc_temperature_data = {}

            for item in data_fc['list']:
                datee = item['dt_txt'].split()[0]

                temp = item['main']['temp']

                if temp in fc_temperature_data:
                    if temp > fc_temperature_data[datee]['max_temp']:
                        fc_temperature_data[datee]['max_temp'] = temp
                    if temp < fc_temperature_data:
                        fc_temperature_data[datee]['min_temp'] = temp
                else:
                    fc_temperature_data[datee] = {'max_temp': temp, 'min_temp': temp}

            for datee, temps in fc_temperature_data.items():
                all_data_combined = f"Date: {datee} \n     Max Temp: {temps['max_temp']} K \n     Min Temp: {temps['min_temp']} K"
            
            print(all_data_combined)
            
            
            start = date.today()

            k = 6

            res = []

            for day in range(k):
                date = (start + datetime.timedelta(days = day)).isoformat()
                res.append(date)

            dates_data = {
                'date1': res[0],
                'date2': res[1],
                'date3': res[2],
                'date4': res[3],
                'date5': res[4]
            }

            return render_template('weather.html', weather=weather_data, forecast_data=all_data_combined, latitude=latitude, api_key=api_key, city_id=city_id, dates_data=dates_data)
        else:
            error_message = data['message']
            return render_template('weather.html', error=error_message)
    return render_template('weather.html')

def forecase_weather():
    api_key1 = api_key
    return print(api_key1)

if __name__ == '__main__':
    app.run(debug=True)
