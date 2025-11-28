import requests 
import time 
import random 
import os 
import sys 
from datetime import datetime 

print("CAN Camera Simulator - Background Worker") 
print("Running in TEST MODE") 
print("Press Ctrl+C to stop") 

class CameraSimulator: 
    def __init__(self): 
        self.supabase_url = os.getenv('SUPABASE_URL', 'TEST_MODE') 
        self.supabase_key = os.getenv('SUPABASE_KEY', 'TEST_MODE') 
        self.session = requests.Session() 
        self.event_count = 0 
        # Use ACTUAL lot IDs from Person A's database: 1, 2, 3
        self.parking_lots = [1, 2, 3]

    def send_parking_event(self, lot_id, delta): 
        if self.supabase_url == 'TEST_MODE': 
            print(f"?? [SIMULATED] Event {self.event_count}: lot_{lot_id}, delta={delta}") 
            return True 

        # Use lot_id directly (already 1, 2, or 3 from Person A's database)
        payload = {
            "lot_id": lot_id,  # Already the correct number
            "delta": delta
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.supabase_key}"
        }
        
        try:
            response = self.session.post(
                self.supabase_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"SUCCESS: Event {self.event_count}: lot_{lot_id} delta={delta}")
                return True
            else:
                print(f"ERROR: HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"ERROR: Request failed: {e}")
            return False

    def run(self): 
        print("Starting simulation...") 
        try: 
            while True: 
                wait_time = random.uniform(30, 60) 
                print(f"WAITING: {wait_time:.1f} seconds until next event...")
                time.sleep(wait_time) 

                lot_id = random.choice(self.parking_lots) 
                delta = random.choice([-1, 1]) 

                if self.send_parking_event(lot_id, delta): 
                    self.event_count += 1 

                if self.event_count % 5 == 0: 
                    print(f"STATUS: Total REAL events sent: {self.event_count}") 

        except KeyboardInterrupt: 
            print(f"STOPPED: Simulation ended. Total events: {self.event_count}") 

if __name__ == "__main__": 
    simulator = CameraSimulator()
    simulator.run()