import requests
import time
import random
import os
import sys
from datetime import datetime

print(" CAN Camera Simulator - Render Optimized")
print(" Running in TEST MODE")
print(" Adjusted for cloud performance")

class CameraSimulator:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'TEST_MODE')
        self.supabase_key = os.getenv('SUPABASE_KEY', 'TEST_MODE')
        self.session = requests.Session()
        self.event_count = 0
        self.parking_lots = ["parking_north", "parking_south", "parking_east", "parking_west"]
    
    def send_parking_event(self, lot_id, delta):
        if self.supabase_url == 'TEST_MODE':
            print(f" [SIMULATED] Event {self.event_count}: {lot_id}, delta={delta}")
            return True
            
        try:
            payload = {"lot_id": lot_id, "delta": delta}
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.supabase_key}"
            }
            
            response = self.session.post(self.supabase_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f" Real Event {self.event_count}: {lot_id} delta={delta}")
                return True
            else:
                print(f" HTTP Error {response.status_code}")
                return False
                
        except Exception as e:
            print(f" Request failed: {e}")
            return False
    
    def run(self):
        print(" Starting simulation (SLOWER VERSION)...")
        
        try:
            while True:
                # SLOWER: Wait 30-60 seconds between events (not 3-8)
                wait_time = random.uniform(30, 60)
                print(f" Waiting {wait_time:.1f} seconds until next event...")
                time.sleep(wait_time)
                
                lot_id = random.choice(self.parking_lots)
                delta = random.choice([-1, 1])
                
                if self.send_parking_event(lot_id, delta):
                    self.event_count += 1
                
                # Status update every 5 events
                if self.event_count % 5 == 0:
                    print(f" Total events: {self.event_count}")
                    
        except KeyboardInterrupt:
            print(f"\n Simulation stopped. Total events: {self.event_count}")

if __name__ == "__main__":
    simulator = CameraSimulator()
    simulator.run()
