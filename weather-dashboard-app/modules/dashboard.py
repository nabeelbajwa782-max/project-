import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import urllib.parse

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Weather Dashboard", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        # Search Frame
        search_frame = tk.Frame(self, bg=controller.bg_color)
        search_frame.pack(pady=10)
        
        self.city_entry = tk.Entry(search_frame, font=("Segoe UI", 14), width=25)
        self.city_entry.grid(row=0, column=0, padx=10)
        self.city_entry.insert(0, "London")
        
        search_btn = tk.Button(search_frame, text="Search City", font=("Segoe UI", 12), bg=controller.accent_color, fg="white", command=self.search_weather)
        search_btn.grid(row=0, column=1)
        
        # Current Weather Frame
        self.current_frame = tk.Frame(self, bg="#2D2D30", bd=2, relief="groove")
        self.current_frame.pack(pady=10, padx=20, fill="x")
        
        self.city_name_lbl = tk.Label(self.current_frame, text="City Name", font=("Segoe UI", 18, "bold"), bg="#2D2D30", fg=controller.fg_color)
        self.city_name_lbl.pack(pady=5)
        
        self.temp_lbl = tk.Label(self.current_frame, text="-- °C", font=("Segoe UI", 36, "bold"), bg="#2D2D30", fg=controller.accent_color)
        self.temp_lbl.pack(pady=5)
        
        self.details_lbl = tk.Label(self.current_frame, text="Wind: -- km/h | Humidity: -- %", font=("Segoe UI", 12), bg="#2D2D30", fg=controller.fg_color)
        self.details_lbl.pack(pady=10)
        
        # Forecast Frame
        forecast_lbl = tk.Label(self, text="7-Day Forecast", font=("Segoe UI", 16, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        forecast_lbl.pack(pady=10)
        
        self.forecast_container = tk.Frame(self, bg=controller.bg_color)
        self.forecast_container.pack(pady=10, padx=20, fill="x")
        
        self.forecast_widgets = []
        for i in range(7):
            f = tk.Frame(self.forecast_container, bg="#2D2D30", bd=1, relief="ridge", width=100, height=120)
            f.pack_propagate(False)
            f.pack(side="left", expand=True, padx=5)
            
            day_lbl = tk.Label(f, text=f"Day {i+1}", font=("Segoe UI", 12), bg="#2D2D30", fg="white")
            day_lbl.pack(pady=10)
            
            t_lbl = tk.Label(f, text="-- / --", font=("Segoe UI", 14, "bold"), bg="#2D2D30", fg=controller.accent_color)
            t_lbl.pack(pady=10)
            
            self.forecast_widgets.append((day_lbl, t_lbl))
            
        self.search_weather()
        
    def _fetch_json(self, url):
        # Using curl via subprocess to bypass broken urllib/requests in user's environment
        try:
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except Exception as e:
            print("cURL error:", e)
            return None
        
    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
            
        self.city_name_lbl.config(text=f"Searching for {city}...")
        self.temp_lbl.config(text="-- °C")
        
        try:
            # 1. Geocoding
            encoded_city = urllib.parse.quote(city)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1"
            
            geo_data = self._fetch_json(geo_url)
                
            if not geo_data or "results" not in geo_data or len(geo_data["results"]) == 0:
                self.city_name_lbl.config(text="City not found")
                return
                
            result = geo_data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            resolved_name = f"{result['name']}, {result.get('country', '')}"
            self.city_name_lbl.config(text=resolved_name)
            
            # 2. Weather Data
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
            
            weather_data = self._fetch_json(weather_url)
            if not weather_data:
                self.city_name_lbl.config(text="Error parsing weather data")
                return
                
            current = weather_data.get("current", {})
            temp = current.get("temperature_2m", "--")
            wind = current.get("wind_speed_10m", "--")
            humidity = current.get("relative_humidity_2m", "--")
            
            self.temp_lbl.config(text=f"{temp} °C")
            self.details_lbl.config(text=f"Wind: {wind} km/h | Humidity: {humidity} %")
            
            daily = weather_data.get("daily", {})
            times = daily.get("time", [])
            t_max = daily.get("temperature_2m_max", [])
            t_min = daily.get("temperature_2m_min", [])
            
            for i in range(min(7, len(times))):
                date_str = times[i][5:] # Skip year, show MM-DD
                max_t = t_max[i]
                min_t = t_min[i]
                
                day_lbl, t_lbl = self.forecast_widgets[i]
                day_lbl.config(text=date_str)
                t_lbl.config(text=f"{max_t}° / {min_t}°")
                
        except Exception as e:
            self.city_name_lbl.config(text="Error fetching data")
            print("Weather error:", e)

    def on_show(self):
        pass
