from flask import Flask, request, jsonify
from zeep import Client, helpers
from datetime import date

# ------------------------------------------------------------------
# WSDL URL – this is the contract that describes the API.
WSDL_URL = "https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl"
client = Client(wsdl=WSDL_URL)
service = client.create_service(
    "{http://localhost/xml/wsdl/ndfdXML.wsdl}ndfdXMLBinding",
    "https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php",
)
# Flask Application
app = Flask(__name__)


# ------------------------------------------------------------------
def get_weather_details(latitude, longitude):
    weather_data = service.NDFDgenByDay(
        latitude, longitude, date.today(), 1, "e", "DWML", "24 hourly"
    )

    print("\nWeather Forecast")

    print("\nWeather Forecast:")
    print(f"Latitude     : {latitude}")
    print(f"Longitude    : {longitude}")
    print(f"Forecast Date: {date.today()}")
    print(f"Weather Data : {weather_data}")

    return weather_data


# GET endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Service is active!"})


# POST endpoint
@app.route("/weather", methods=["POST"])
def get_weather():

    try:
        data = request.get_json()

        if not data or "latitude" not in data:
            return jsonify({"error": "Invalid Latitude"}), 400

        if "longitude" not in data:
            return jsonify({"error": "Invalid Longitude"}), 400

        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        if not -90 <= latitude <= 90:
            return jsonify({"error": "Latitude must be between -90 and 90."}), 400

        if not -180 <= longitude <= 180:
            return jsonify({"error": "Longitude must be between -180 and 180."}), 400

        result = get_weather_details(latitude, longitude)

        return jsonify(
            {"latitude": latitude, "longitude": longitude, "weather_forecast": result}
        )
    except Exception as exc:
        return jsonify({"error": f"Unable to retrieve weather information: {exc}"}), 400


# Run Application
if __name__ == "__main__":

    app.run(debug=True)
