import random
import time

SPEED_LIMIT = 80
VEHICLE_LIMIT = 40

def generate_gps_data():
    latitude = random.uniform(12.9000, 13.1000)
    longitude = random.uniform(80.2000, 80.3000)
    speed = random.randint(20, 120)
    vehicle_count = random.randint(5, 60)
    return latitude, longitude, speed, vehicle_count

def threshold_check(speed, vehicle_count):
    if speed > SPEED_LIMIT:
        return "Overspeed Detected"
    elif vehicle_count > VEHICLE_LIMIT:
        return "Congestion Detected"
    else:
        return "Normal Traffic"

def signal_decision(status):
    if status == "Congestion Detected":
        return "Increase Green Signal Time to 90 seconds"
    else:
        return "Normal Green Signal Time (60 seconds)"

while True:
    lat, lon, speed, vehicles = generate_gps_data()
    
    status = threshold_check(speed, vehicles)
    decision = signal_decision(status)

    print("\nGPS DATA")
    print("Latitude:", round(lat, 5))
    print("Longitude:", round(lon, 5))
    print("Speed:", speed, "km/h")
    print("Vehicle Count:", vehicles)
    print("Status:", status)
    print("Signal Decision:", decision)
    print("-----------------------------------")

    time.sleep(1)