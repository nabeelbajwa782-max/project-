import base64
import zlib
import subprocess
import os

def kroki_url(diagram_type, text):
    compressed = zlib.compress(text.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return f"https://kroki.io/{diagram_type}/png/{encoded}"

def download_png(text, filepath):
    url = kroki_url('mermaid', text)
    try:
        subprocess.run(['curl', '-s', '-o', filepath, url], check=True)
        print(f"Saved {filepath}")
    except Exception as e:
        print(f"Failed to save {filepath}: {e}")

component_diagram = """
graph TD
    subgraph Client
        UI[Tkinter Desktop App]
    end

    subgraph Microservices Backend
        WS[Weather Service - Port 8001]
        TS[Task & Notes Service - Port 8002]
        AS[Analytics Service - Port 8003]
    end

    subgraph Data Sources
        DB[(SQLite app.db)]
        API[Open-Meteo API]
    end

    UI -->|HTTP GET| WS
    UI -->|HTTP GET/POST/DELETE| TS
    UI -->|HTTP GET/POST| AS

    WS -->|HTTP| API
    TS -->|SQL| DB
    AS -->|SQL| DB
"""

sequence_diagram = """
sequenceDiagram
    actor User
    participant App as Tkinter App (Dashboard)
    participant WS as Weather Service (8001)
    participant OM as Open-Meteo API

    User->>App: Enters City & Clicks Search
    App->>WS: HTTP GET /weather?city={City}
    WS->>OM: HTTP GET Geocoding API
    OM-->>WS: JSON (Latitude, Longitude)
    WS->>OM: HTTP GET Weather Forecast API
    OM-->>WS: JSON (Current, Daily Forecast)
    WS-->>App: JSON (Parsed Weather Data)
    App-->>User: Updates UI with Temp & Forecast
"""

class_diagram = """
classDiagram
    class WeatherDashboardApp {
        +frames: dict
        +show_frame(name: str)
    }

    class DashboardFrame {
        +search_weather()
    }

    class PlannerFrame {
        +load_tasks()
        +add_task()
        +delete_task()
    }

    class TaskService {
        +GET /tasks
        +POST /tasks
        +DELETE /tasks
    }
    
    class AnalyticsService {
        +GET /analytics
        +POST /sessions
    }

    WeatherDashboardApp --> DashboardFrame
    WeatherDashboardApp --> PlannerFrame
    DashboardFrame ..> "HTTP" TaskService : depends on
    PlannerFrame ..> "HTTP" TaskService : depends on
"""

if __name__ == "__main__":
    download_png(component_diagram, "docs/uml/component/component_diagram.png")
    download_png(sequence_diagram, "docs/uml/sequence/sequence_diagram.png")
    download_png(class_diagram, "docs/uml/class/class_diagram.png")
