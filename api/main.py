from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        location = request.form['location']
        api_key = 'c70f6f3bf64ab7edc365a23b47a6f5d6' 
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response = requests.get(url)
        print(url)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                'location': data['name'],
                'temperature': round(data['main']['temp']),
                'condition': data['weather'][0]['description'],
                'FeelsLike': round(data['main']['feels_like'])
            }
            return render_template('weather.html', weather=weather_data)
        else:
            error_message = data['message']
            return render_template('weather.html', error=error_message)
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)
