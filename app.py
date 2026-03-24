from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "9e95cd0dd4c8a003f8aeb739fef20082"   # 👈 apni API key daal


# 🟢 HOME (CITY SEARCH)
@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        try:
            # 🔥 CURRENT WEATHER
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            weather_data = requests.get(weather_url).json()

            if weather_data.get("cod") != 200:
                error = "City not found"
            else:
                weather = {
                    "city": weather_data["name"],
                    "temp": weather_data["main"]["temp"],
                    "desc": weather_data["weather"][0]["description"],
                    "humidity": weather_data["main"]["humidity"],
                    "wind": weather_data["wind"]["speed"]
                }

                # 🔥 FORECAST API
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                forecast_data = requests.get(forecast_url).json()

                forecast = []
                for i in range(0, 40, 8):  # 5 days
                    day = forecast_data['list'][i]
                    forecast.append({
                        "day": day['dt_txt'].split(" ")[0],
                        "temp": round(day['main']['temp'])
                    })

        except Exception as e:
            error = "Something went wrong"
            print(e)

    return render_template("index.html", weather=weather, forecast=forecast, error=error)


# 📍 LOCATION ROUTE (FULL FIXED)
@app.route("/location")
def location():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    weather = None
    forecast = None
    error = None

    try:
        # 🔥 CURRENT WEATHER
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()

        if weather_data.get("cod") != 200:
            error = "Location not found"
        else:
            weather = {
                "city": weather_data["name"],
                "temp": weather_data["main"]["temp"],
                "desc": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind": weather_data["wind"]["speed"]
            }

            # 🔥 FORECAST API (FIX ADDED)
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_data = requests.get(forecast_url).json()

            forecast = []
            for i in range(0, 40, 8):  # 5 days
                day = forecast_data['list'][i]
                forecast.append({
                    "day": day['dt_txt'].split(" ")[0],
                    "temp": round(day['main']['temp'])
                })

    except Exception as e:
        error = "Something went wrong"
        print(e)

    return render_template("index.html", weather=weather, forecast=forecast, error=error)


if __name__ == "__main__":
    app.run(debug=True)
