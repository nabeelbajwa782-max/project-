from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import urllib.parse

class WeatherHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _fetch_json(self, url):
        try:
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except Exception as e:
            print("cURL error:", e)
            return None

    def do_GET(self):
        if self.path.startswith('/weather?city='):
            city = urllib.parse.unquote(self.path.split('=')[1])
            encoded_city = urllib.parse.quote(city)
            
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1"
            geo_data = self._fetch_json(geo_url)
            
            if not geo_data or "results" not in geo_data or len(geo_data["results"]) == 0:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "City not found"}).encode())
                return
                
            result = geo_data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            resolved_name = f"{result['name']}, {result.get('country', '')}"
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
            weather_data = self._fetch_json(weather_url)
            
            if not weather_data:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": "Weather fetch failed"}).encode())
                return
                
            response_data = {
                "city": resolved_name,
                "current": weather_data.get("current", {}),
                "daily": weather_data.get("daily", {})
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

def run(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WeatherHandler)
    print(f"Weather Service running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
