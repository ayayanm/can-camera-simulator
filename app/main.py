import requests 
import time 
import random 
import os 
import sys 
from datetime import datetime 
from flask import Flask
import threading

print("CAN Camera Simulator - Background Worker with Health Check") 
print("Running in TEST MODE") 
print("Press Ctrl+C to stop") 

# Create Flask app for health checks
app = Flask(__name__)
simulator = None

@app.route('/')
def health_check():
    if simulator:
        return {'status': 'healthy', 'events': simulator.event_count}
    return {'status': 'starting'}

@app.route('/health')
def health():
    return 'OK', 200

class CameraSimulator: 
    def __init__(self): 
        self.supabase_url = os.getenv('SUPABASE_URL', 'TEST_MODE') 
        self.supabase_key = os.getenv('SUPABASE_KEY', 'TEST_MODE') 
        self.session = requests.Session() 
        self.event_count = 0 
        self.parking_lots = ["parking_north", "parking_south", "parking_east", "parking_west"] 

    def send_parking_event(self, lot_id, delta): 
        if self.supabase_url == 'TEST_MODE': 
            print(f"?? [SIMULATED] Event {self.event_count}: {lot_id}, delta={delta}") 
            return True 

        try: 
            payload = {"lot_id": lot_id, "delta": delta} 
            headers = { 
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {self.supabase_key}" 
            } 

            response = self.session.post(self.supabase_url, json=payload, headers=headers, timeout=10) 

            if response.status_code == 200: 
                print(f"? Real Event {self.event_count}: {lot_id} delta={delta}") 
                return True 
            else: 
                print(f"HTTP Error {response.status_code}") 
            return False 

        except Exception as e: 
            print(f"? Request failed: {e}") 
            return False 

    def run(self): 
        print("Starting simulation...") 

        try: 
            while True: 
                wait_time = random.uniform(3, 8) 
                time.sleep(wait_time) 

                lot_id = random.choice(self.parking_lots) 
                delta = random.choice([-1, 1]) 

                if self.send_parking_event(lot_id, delta): 
                    self.event_count += 1 

                if self.event_count % 5 == 0: 
                    print(f" Total events: {self.event_count}") 

        except KeyboardInterrupt: 
            print(f"\n Simulation stopped. Total events: {self.event_count}") 

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

if __name__ == "__main__": 
    # Start the simulator
    simulator = CameraSimulator()
    
    # Start Flask in a separate thread (for health checks)
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run the main simulation
    simulator.run()