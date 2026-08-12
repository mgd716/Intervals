import os
import requests
import time
import math
import datetime
from requests.auth import HTTPBasicAuth
from supabase import create_client, Client

# ==================== CONFIGURATION ====================
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")
API_KEY = os.getenv("INTERVALS_API_KEY")
# Using .strip() to remove any accidental hidden spaces or newlines
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
# =======================================================

def fetch_activities():
    base_url = "https://intervals.icu/"
    endpoint = f"api/v1/athlete/{ATHLETE_ID}/activities"
    params = {"oldest": "2010-01-01", "newest": "2030-01-01"}
    response = requests.get(base_url + endpoint, params=params, auth=HTTPBasicAuth('API_KEY', API_KEY))
    if response.status_code != 200:
        raise Exception(f"Failed to fetch activities list: {response.status_code}")
    return response.json()

def fetch_gps_stream(activity_id):
    base_url = "https://intervals.icu/"
    endpoint = f"api/v1/activity/{activity_id}/streams.json"
    params = {"types": "latlng"}
    response = requests.get(base_url + endpoint, params=params, auth=HTTPBasicAuth('API_KEY', API_KEY))
    
    if response.status_code == 200:
        streams = response.json()
        if isinstance(streams, list):
            for stream in streams:
                if isinstance(stream, dict) and stream.get("type") == "latlng":
                    lats = stream.get("data", [])
                    lngs = stream.get("data2", [])
                    if lats and lngs:
                       return [[round(lat, 5), round(lng, 5)] for lat, lng in zip(lats, lngs) if lat is not None and lng is not None][::4]
    return None
    
def get_tile(lat, lon, zoom):
    """Converts Latitude/Longitude to standard map tile X/Y coordinates"""
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return f"{zoom}_{xtile}_{ytile}"

def fetch_wellness_data(days_back=14):
    """Fetches daily wellness records (including steps) from Intervals.icu"""
    base_url = "https://intervals.icu/"
    today = datetime.date.today()
    oldest = today - datetime.timedelta(days=days_back)
    
    endpoint = f"api/v1/athlete/{ATHLETE_ID}/wellness?oldest={oldest}&newest={today}"
    response = requests.get(base_url + endpoint, auth=HTTPBasicAuth('API_KEY', API_KEY))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch wellness data: {response.status_code}")
        return []

def sync_steps_to_supabase(days_back=14):
    wellness_records = fetch_wellness_data(days_back)
    print(f"Processing steps for the last {len(wellness_records)} wellness entries...")
    
    for record in wellness_records:
        entry_date = record.get("id") # Format: "YYYY-MM-DD"
        steps = record.get("steps")
        
        # Only update if step data is available for that day
        if entry_date and steps is not None:
            supabase.table("macro_logs").upsert({
                "date": entry_date,   # Assumes 'date' is your primary/unique key on macro_logs
                "steps": int(steps)
            }, on_conflict="date").execute()

    print("Steps sync complete!")

def main():
    # --- Debugging Block ---
    print("--- Credential Check ---")
    print(f"ATHLETE_ID: {'Loaded' if ATHLETE_ID else 'Missing'}")
    print(f"API_KEY: {'Loaded' if API_KEY else 'Missing'}")
    print(f"SUPABASE_URL: '{SUPABASE_URL}'")
    print(f"SUPABASE_KEY: {'Loaded' if SUPABASE_KEY else 'Missing'}")
    print("------------------------")

    if not all([ATHLETE_ID, API_KEY, SUPABASE_URL, SUPABASE_KEY]):
        print("Error: Missing credentials. Check your GitHub Secrets!")
        return
        
    if not SUPABASE_URL.startswith("http"):
        print("Error: SUPABASE_URL must start with http:// or https://")
        return

    try:
        # We initialize the client HERE so the script can validate the strings first
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 1. Fetch ALL existing IDs by paginating in chunks of 1000
        existing_ids = set()
        start = 0
        chunk_size = 1000
        
        while True:
            response = supabase.table("activities").select("id").range(start, start + chunk_size - 1).execute()
            if not response.data:
                break
            for row in response.data:
                existing_ids.add(str(row["id"]))
            start += chunk_size
        
        activities = fetch_activities()
        print(f"Checking {len(activities)} total activities against {len(existing_ids)} in database...")
        
        new_downloads = 0
        
        for idx, act in enumerate(activities):
            act_id = str(act.get("id"))
            
            if act_id in existing_ids:
                continue
                
            act_type = act.get("type", "Other")
            act_name = act.get("name", f"Activity {act_id}")
            act_date = act.get("start_date_local", "")
            act_year = int(act_date.split("-")[0]) if act_date else 0
                
            print(f"[{idx+1}/{len(activities)}] Processing: {act_name}")
            coordinates = fetch_gps_stream(act_id)
            
            # If there's no GPS stream (indoor/virtual/gym), default to an empty list
            if not coordinates:
                coordinates = []
                activity_tiles = []
            else:
                # Calculate unique tiles ONLY if coordinates exist
                activity_tiles = set()
                for lat, lng in coordinates:
                    activity_tiles.add(get_tile(lat, lng, 14)) # Squadrat
                    activity_tiles.add(get_tile(lat, lng, 17)) # Squadratinho
                activity_tiles = list(activity_tiles)

            new_downloads += 1
            
            # UPSERT runs for ALL activities now, with or without GPS coordinates
            supabase.table("activities").upsert({
                "id": act_id,
                "type": act_type,
                "name": act_name,
                "year": act_year,
                "start_date": act.get("start_date_local", ""),
                "distance": act.get("distance", 0.0),
                "moving_time": act.get("moving_time", 0),
                "elapsed_time": act.get("elapsed_time", 0),
                "calories": act.get("calories", 0),
                "total_elevation_gain": act.get("total_elevation_gain", 0.0),
                "max_elevation": act.get("elev_high", 0.0),
                "tss": act.get("tss", 0.0),
                
                # Performance Metrics
                "average_heartrate": act.get("average_heartrate", 0.0),
                "max_heartrate": act.get("max_heartrate", 0.0),
                "average_watts": act.get("average_watts") or act.get("icu_weighted_avg_watts", 0.0),
                "average_cadence": act.get("average_cadence", 0.0),
                "work": act.get("work", 0.0),
                
                "coordinates": coordinates,
                "raw_data": act,
                "visited_tiles": activity_tiles
            }).execute()
            
            time.sleep(0.2)

        print(f"\nSuccess! Inserted {new_downloads} new tracks into the database.")

    


        
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
