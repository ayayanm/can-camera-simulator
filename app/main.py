import requests
import time
import random
import os
import sys
from datetime import datetime

print("CAN Camera Simulator - PRODUCTION MODE")
print("Checking for Supabase credentials...")

class CameraSimulator:
    def __init__(self):
        # CRITICAL FIX: Remove default 'TEST_MODE' values
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        # VALIDATE CREDENTIALS
        if not self.supabase_url or not self.supabase_key:
            print("ERROR: Missing Supabase credentials!")
            print("Please set SUPABASE_URL and SUPABASE_KEY in Render Environment")
            print("Current SUPABASE_URL:", self.supabase_url)
            print("Current SUPABASE_KEY:", "Set" if self.supabase_key else "Missing")
            sys.exit(1)  # STOP if credentials missing
            
        print("SUPABASE: Credentials found!")
        print("SUPABASE: URL:", self.supabase_url)
        
        self.session = requests.Session()
        self.event_count = 0
        self.parking_lots = ["parking_north", "parking_south", "parking_east", "parking_west"]
    
    def send_parking_event(self, lot_id, delta):
        # NOW IT WILL ONLY USE REAL MODE
        payload = {"lot_id": lot_id, "delta": delta}
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
                print(f"SUCCESS: Event {self.event_count}: {lot_id} delta={delta}")
                return True
            else:
                print(f"ERROR: HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"ERROR: Request failed: {e}")
            return False
    
    def run(self):
        print("STARTING: Production simulation...")
        print("SENDING: Real events to Supabase!")
        
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
