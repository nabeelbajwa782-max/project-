# Weather Dashboard - Microservices Architecture & UML

## 1. Component Diagram
This diagram shows the transition from a monolithic architecture to a microservices-based architecture. The Tkinter Desktop App acts as a thin client, making HTTP REST API calls to the backend microservices.

```mermaid
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
```

## 2. Sequence Diagram
This sequence diagram illustrates the flow of data when a user searches for weather.

```mermaid
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
```

## 3. Class Diagram
This class diagram highlights the logical separation between the UI presentation layer and the microservices layer.

```mermaid
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
```

## 4. Use Case Diagram
`mermaid
graph LR
    User([User])
    subgraph Weather Dashboard App
        W[Search Weather Forecast]
        T[Manage Study Tasks]
        N[Write & Manage Notes]
        F[Run Focus Timer]
        A[View Productivity Analytics]
    end
    User --> W
    User --> T
    User --> N
    User --> F
    User --> A
`

## 5. Activity Diagram
`mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running : User clicks Start
    Running --> Running : Time ticking down
    Running --> Paused : User clicks Stop
    Paused --> Running : User clicks Start
    Running --> SessionComplete : Timer reaches 00:00
    state SessionComplete {
        [*] --> SaveSession
        SaveSession --> ShowNotification
        ShowNotification --> [*]
    }
    SessionComplete --> Idle
`
