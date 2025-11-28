import requests 
import time 
import random 
import os 
import sys 
from datetime import datetime 

print(" CAN Camera Simulator - ULTIMATE DEBUG MODE") 
print(" Running in TEST MODE") 
print(" Press Ctrl+C to stop") 

class CameraSimulator: 
    def __init__(self): 
        self.supabase_url = os.getenv('SUPABASE_URL', 'TEST_MODE') 
        self.supabase_key = os.getenv('SUPABASE_KEY', 'TEST_MODE') 
        self.session = requests.Session() 
        self.event_count = 0 
        # Use ACTUAL lot IDs from Person A's database: 1, 2, 3
        self.parking_lots = [1, 2, 3]
        
        print(f" INIT: Supabase URL: {self.supabase_url}")
        print(f" INIT: Supabase Key set: {'YES' if self.supabase_key else 'NO'}")

    def send_parking_event(self, lot_id, delta): 
        if self.supabase_url == 'TEST_MODE': 
            print(f"?? [SIMULATED] Event {self.event_count}: lot_{lot_id}, delta={delta}") 
            return True 

        print(f" DEBUG: Supabase URL: {self.supabase_url}")
        print(f" DEBUG: lot_id: {lot_id} (type: {type(lot_id).__name__})")
        print(f" DEBUG: delta: {delta} (type: {type(delta).__name__})")
        
        # Force convert to integers to be 100% sure
        lot_id_int = int(lot_id)
        delta_int = int(delta)
        
        print(f" DEBUG: After conversion - lot_id: {lot_id_int} (type: {type(lot_id_int).__name__})")
        print(f" DEBUG: After conversion - delta: {delta_int} (type: {type(delta_int).__name__})")
        
        payload = {
            "lot_id": lot_id_int,
            "delta": delta_int
        }
        
        print(f" DEBUG: Final payload: {payload}")
        print(f" DEBUG: Payload as JSON string: {repr(str(payload))}")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.supabase_key}"
        }
        
        try:
            print(f" DEBUG: Sending request to: {self.supabase_url}")
            response = self.session.post(
                self.supabase_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            print(f" DEBUG: Response status: {response.status_code}")
            print(f" DEBUG: Response text: {response.text}")
            
            if response.status_code == 200:
                print(f" SUCCESS: Event {self.event_count}: lot_{lot_id} delta={delta}")
                return True
            else:
                print(f" ERROR: HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f" ERROR: Request failed: {e}")
            return False

    def run(self): 
        print(" Starting simulation...") 
        try: 
            while True: 
                wait_time = random.uniform(30, 60) 
                print(f" WAITING: {wait_time:.1f} seconds until next event...")
                time.sleep(wait_time) 

                lot_id = random.choice(self.parking_lots) 
                delta = random.choice([-1, 1]) 

                if self.send_parking_event(lot_id, delta): 
                    self.event_count += 1 

                if self.event_count % 5 == 0: 
                    print(f"📊 STATUS: Total REAL events sent: {self.event_count}") 

        except KeyboardInterrupt: 
            print(f" STOPPED: Simulation ended. Total events: {self.event_count}") 

if __name__ == "__main__": 
    simulator = CameraSimulator()
    simulator.run()