from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes
import requests
from datetime import datetime
from adhanpy.calculation import CalculationMethod

# Initializing values
api_key = ""
today = datetime.now()
address = input("Enter your location: ")
timestamp = int(datetime.now().timestamp())
url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {
    "address": address,
    "key": api_key }
# method = input("1. Muslim World League\n2.Egypt\n3.Karachi\n4.Umm Al Qura\n5.Dubai\n6.Moon Sighting Committee\n7.North America\n8.Kuwait\n9.Qatar\n10.Singapore\n11.UOIF\nEnter the number of the method you would like to use: ")
space = "            "
breaking = "================================================================================================================================================"
method = int(input(f"\n{breaking}\n1. Muslim World League{space}2.Egypt{space}3.Karachi{space}4.Umm Al Qura{space}5.Dubai{space}6.Moon Sighting Committee\n7.North America       {space}8.Kuwait{space}9.Qatar{space}10.Singapore{space}11.Union of Islamic Organizations of France \n{breaking}\n\nEnter the number of the method you would like to use: "))




#DEFINING OUTPUT PROCEDURE
def print_prayer_times(when: datetime, prayer_times: PrayerTimes):
    format = "%H:%M"
    print(f"Prayer times for {today.strftime('%A %d %B %Y')}:")
    print(f"Fajr: {prayer_times.fajr.strftime(format)}")
    print(f"Sunrise: {prayer_times.sunrise.strftime(format)}")
    print(f"Dhuhr: {prayer_times.dhuhr.strftime(format)}")
    print(f"Asr: {prayer_times.asr.strftime(format)}")
    print(f"Maghrib: {prayer_times.maghrib.strftime(format)}")
    print(f"Isha: {prayer_times.isha.strftime(format)}")

#SECTION 1.1: GETTING LAT, LONG
# Make request
response = requests.get(url, params=params)
data = response.json()

if data["status"] == "OK":
    location = data["results"][0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
else:
    print("Error:", data["status"], data.get("error_message"))

#SECTION 1.2: GETTING IANA KEY

# Google Time Zone API endpoint
url = f"https://maps.googleapis.com/maps/api/timezone/json?location={lat},{lng}&timestamp={timestamp}&key={api_key}"

# Make request
response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    timezone_iana = data["timeZoneId"]
else:
    print("Error:", data["status"], data.get("errorMessage"))

#SECTION 2: OUTPUT
coordinates = (lat, lng)
print(CalculationMethod(method))
time_zone = ZoneInfo(timezone_iana)

prayer_times = PrayerTimes(
    coordinates,
    today,
    CalculationMethod(method),
    time_zone=time_zone
)
print_prayer_times(today, prayer_times)