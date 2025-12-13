import os
import csv
import numpy as np
from datetime import datetime
import re

ROOT_DIR = "/Volumes/MacShare/FURUNO_data/PNG_data"
OUTPUT_FILE = "frame_stats.csv"

# Location mappings
# key: lowercase substring or exact match to look for in folder name
# value: Display Name
LOCATION_MAPPING = {
    "portsmouth": "Elizabeth River",
    "elizabeth": "Elizabeth River",
    "grice": "Charleston",
    "greenwood": "Greenwood Lake",
    "monticello": "Monticello Lake",
    "murray": "Murray Lake"
}

def get_display_location(folder_name_part):
    lower_name = folder_name_part.lower()
    for key, val in LOCATION_MAPPING.items():
        if key in lower_name:
            return val
    return folder_name_part # Default to original if no match

def parse_timestamp(filename):
    # Format: YYYYMMDD_HHMMSS_fff_...
    # Example: 20251107_172422_622_72_4.png
    try:
        parts = filename.split('_')
        if len(parts) >= 3:
            date_str = parts[0]
            time_str = parts[1]
            ms_str = parts[2]
            
            full_str = f"{date_str}{time_str}{ms_str}"
            # Format: YYYYMMDDHHMMSSfff (microseconds is %f but this is 3 digits so milliseconds)
            dt = datetime.strptime(full_str, "%Y%m%d%H%M%S%f")
            return dt
    except Exception as e:
        return None
    return None

def calculate_rpm(timestamps):
    if len(timestamps) < 2:
        return None
    
    timestamps.sort()
    deltas = []
    for i in range(1, len(timestamps)):
        diff = (timestamps[i] - timestamps[i-1]).total_seconds()
        if diff <= 5.0: # Ignore gaps > 5 seconds
            deltas.append(diff)
            
    if not deltas:
        return None
        
    avg_delta = np.mean(deltas)
    if avg_delta == 0:
        return 0
    
    # RPM = 60 / avg_delta
    # Usually RPM is an integer like 24, 48, etc.
    # We will round to nearest integer.
    rpm = 60.0 / avg_delta
    return int(round(rpm))

def main():
    # Aggregators
    range_counts = {}
    location_counts = {}
    rpm_counts = {}
    
    print(f"Scanning {ROOT_DIR}...")
    
    if not os.path.exists(ROOT_DIR):
        print(f"Error: Directory {ROOT_DIR} does not exist.")
        return

    subdirs = [d for d in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, d))]
    
    for subdir in subdirs:
        # Parse folder name
        # Format: Location_Date_time_range code_type of data_gain_Max gain_error_code
        parts = subdir.split('_')
        if len(parts) < 4:
            continue # Skip non-conforming folders
            
        raw_location = parts[0]
        # range code is index 3
        range_code = parts[3]
        
        display_location = get_display_location(raw_location)
        
        # Count frames and calculate RPM
        subdir_path = os.path.join(ROOT_DIR, subdir)
        files = [f for f in os.listdir(subdir_path) if f.lower().endswith('.png')]
        frame_count = len(files)
        
        if frame_count == 0:
            continue
            
        # Update Range Counts
        range_counts[range_code] = range_counts.get(range_code, 0) + frame_count
        
        # Update Location Counts
        location_counts[display_location] = location_counts.get(display_location, 0) + frame_count
        
        # Calculate RPM
        timestamps = []
        for f in files:
            ts = parse_timestamp(f)
            if ts:
                timestamps.append(ts)
                
        rpm = calculate_rpm(timestamps)
        
        if rpm is not None:
            rpm_counts[rpm] = rpm_counts.get(rpm, 0) + frame_count
        else:
            # If we couldn't calc RPM (e.g. single file), maybe log as 'Unknown'
            rpm_counts['Unknown'] = rpm_counts.get('Unknown', 0) + frame_count

    # Write CSV
    print(f"Writing results to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['Category', 'Value', 'Frame_Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write Range Data
        for r_code in sorted(range_counts.keys()):
            writer.writerow({'Category': 'Range_Code', 'Value': r_code, 'Frame_Count': range_counts[r_code]})
            
        # Write Location Data
        for loc in sorted(location_counts.keys()):
            writer.writerow({'Category': 'Location', 'Value': loc, 'Frame_Count': location_counts[loc]})
            
        # Write RPM Data
        for rpm in sorted([k for k in rpm_counts.keys() if isinstance(k, int)]):
            writer.writerow({'Category': 'RPM', 'Value': rpm, 'Frame_Count': rpm_counts[rpm]})
            
        # Write Unknown RPM if any
        if 'Unknown' in rpm_counts:
             writer.writerow({'Category': 'RPM', 'Value': 'Unknown', 'Frame_Count': rpm_counts['Unknown']})

    print("Done.")

if __name__ == "__main__":
    main()
