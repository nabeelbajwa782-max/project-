import subprocess
import time
import sys

def main():
    print("Starting Microservices...")
    
    # Run the services as background processes
    weather_proc = subprocess.Popen([sys.executable, "services/weather_service.py"])
    task_proc = subprocess.Popen([sys.executable, "services/task_service.py"])
    analytics_proc = subprocess.Popen([sys.executable, "services/analytics_service.py"])
    
    print("Services are running on ports 8001, 8002, 8003.")
    print("Press Ctrl+C to stop all services.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        weather_proc.terminate()
        task_proc.terminate()
        analytics_proc.terminate()
        print("All services stopped.")

if __name__ == '__main__':
    main()
