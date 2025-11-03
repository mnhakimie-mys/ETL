import os               
import requests          
import pandas as pd      
from datetime import datetime
from dotenv import load_dotenv  

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = [
    "Johor Bahru", "Alor Setar", "Kota Bharu", "Melaka",
    "Seremban", "Kuantan", "Ipoh", "Kangar", "George Town",
    "Kota Kinabalu", "Kuching", "Shah Alam", "Kuala Terengganu",
    "Kuala Lumpur", "Putrajaya", "Labuan"
]

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city + ",MY",      
        "appid": API_KEY,       
        "units": "metric"       
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()

            city_name = data.get("name")
            main = data.get("main", {})
            weather = data.get("weather", [{}])[0]
            wind = data.get("wind", {})
            coord = data.get("coord",{})

            result = {
                "city": city_name,
                "longitude": coord.get("lon"),
                "latitude": coord.get("lat"),
                "temperature": main.get("temp"),
                "temp_min": main.get("temp_min"),
                "temp_max": main.get("temp_max"),
                "humidity": main.get("humidity"),
                "pressure": main.get("pressure"),
                "weather_description": weather.get("description"),
                "wind_speed": wind.get("speed"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(f"{city_name}: {result['temperature']}°C, {result['weather_description']}")
            return result

        else:
            print(f"Cannot fetch {city}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error for {city}: {e}")
        return None

def main():
    print("🌦️ Starting weather data collection...")
    all_records = []

    for city in CITIES:
        record = get_weather(city)
        if record:
            all_records.append(record)

    if all_records:
        df = pd.DataFrame(all_records)
        file_name = "weather_data.csv"
        write_header = not os.path.exists(file_name)
        df.to_csv(file_name, mode='a', index=False, header=write_header, encoding="utf-8-sig")
        print(f"Saved {len(all_records)} new records to {file_name}")

    print("Finished weather data extraction!")

if __name__ == "__main__":
    main()