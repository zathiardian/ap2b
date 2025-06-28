

import flask
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

mock_weather_data = {
    "JAKARTA": {"temp_c": 32, "condition": "Cerah Berawan", "humidity": "75%"},
    "BANDUNG": {"temp_c": 24, "condition": "Hujan Ringan", "humidity": "88%"},
    "SURABAYA": {"temp_c": 34, "condition": "Cerah", "humidity": "70%"},
    "DENPASAR": {"temp_c": 31, "condition": "Cerah", "humidity": "80%"},
    "MEDAN": {"temp_c": 33, "condition": "Badai Petir", "humidity": "85%"},
}
valid_cities = list(mock_weather_data.keys())

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city_param = request.args.get('city')
    delay = random.uniform(0.2, 0.6)
    time.sleep(delay)
    if city_param:
        city = city_param.upper()
        if city in mock_weather_data:
            data = mock_weather_data[city]
            data["city"] = city
            print(f"[SERVER] Sending weather for {city}: {data} (after {delay:.2f}s delay)")
            return jsonify(data)
        else:
            error_msg = {"error": "city_not_found", "message": f"City '{city}' not found in our database."}
            print(f"[SERVER] City {city} not found (after {delay:.2f}s delay)")
            return jsonify(error_msg), 404
    else:
        random_city = random.choice(valid_cities)
        data = mock_weather_data[random_city]
        data["city"] = random_city
        print(f"[SERVER] Sending random weather for {random_city}: {data} (after {delay:.2f}s delay)")
        return jsonify(data)

if __name__ == '__main__':
    print("Simple Weather Forecast API Server running on http://127.0.0.1:5000")
    print("Endpoint: GET /get_weather (opsional: ?city=JAKARTA)")
    app.run(debug=False, threaded=True, use_reloader=False)
