# Weather Dashboard Desktop Application

This is a Python Tkinter desktop application that helps students improve productivity and study efficiency using AI-inspired scheduling and tracking features.

## Project Structure

- `docs/`: Documentation and UML diagrams (Mermaid format and PNG images).
- `microservices/`: Independent backend services for Weather, Tasks/Notes, and Analytics.
- `src/`: The main Tkinter desktop application client.
- `tests/`: Unit tests for the application logic and database layer.

## How to Run

Since the application has been refactored into a microservices architecture, you must run the backend services before launching the frontend GUI.

1. **Start the Microservices:**
   ```bash
   python start_services.py
   ```
   This will start the Weather Service (8001), Task Service (8002), and Analytics Service (8003).

2. **Launch the Desktop Client:**
   Open a new terminal window and run:
   ```bash
   python src/main.py
   ```

## Technologies
- **Python 3**
- **Tkinter** for the native Desktop GUI.
- **SQLite** for local database storage.
- **Python http.server** for dependency-free microservices.
